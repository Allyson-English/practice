import sqlalchemy
import pandas as pd

# Import CSV of Nairobi traffic data
full_dataset = pd.read_csv('working_data_7_days.csv', low_memory=False)

w_index = full_dataset.reset_index()
w_index.head(2)

# Creates speeds table, osm_way_id is foreign key, index is primary key
speeds = w_index[
    [
        'index',
        'osm_way_id',
        'year',
        'quarter',
        'hour_of_day', 
        'speed_kph_mean',
        'speed_kph_stddev', 
        'speed_kph_p85'
    ]
].set_index('index')

# Creates road attribute table and removes duplicate entries by osm_way_id
# osm_way_id is primary key
road_attrs = w_index[
    ['osm_way_id', 'road_name', 'road_type', 'one_way', 'surface']
].drop_duplicates('osm_way_id').set_index('osm_way_id')

# Check to see if there are any null values in the speeds table
for c in speeds.columns:
    if speeds[c].isna().sum() != 0:
        print(f"Column: {c} has null values in it.")
        
        
db_path = '.../nairobi_uber_speeds.db'
engine = sqlalchemy.create_engine(f'sqlite:///{db_path}')

speeds.dtypes

# Creating speeds table

with engine.connect() as conn:

    try:
        conn.execute("DROP TABLE speeds;")
    except:
        print("The speeds table does not exist yet.")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS speeds
        ('index' INT PRIMARY KEY NOT NULL,
        'osm_way_id' INT NOT NULL,
        'year' INT NOT NULL,
        'quarter' INT NOT NULL,
        'hour_of_day' INT NOT NULL, 
        'speed_kph_mean' REAL NOT NULL,
        'speed_kph_stddev' REAL NOT NULL, 
        'speed_kph_p85' REAL NOT NULL);
    """)
    
    # Makes a 'binary tree index' on osm_way_id column to improve efficiency when joining on rows table
    conn.execute('CREATE INDEX osm_idx ON speeds(osm_way_id);')
    

# Describes variables in table 

with engine.connect() as conn:
    query = "PRAGMA table_info([speeds]);"
    
    df = pd.read_sql(query, conn)
    display(df)
    
    query = "PRAGMA index_list('speeds');"
    
    df = pd.read_sql(query, conn)
    display(df)
    
    
with engine.connect() as conn:
    speeds.to_sql('speeds', conn, if_exists='append')
    
# Simple query to make sure everything is running smoothly (it is!) 

with engine.connect() as conn:
    query = "SELECT * FROM speeds LIMIT 3;"
    df = pd.read_sql(query, conn)
df

# Check that total number of observations in speeds table equals that in original dataset

with engine.connect() as conn:
    query = "SELECT COUNT(*) FROM speeds;"
    df = pd.read_sql(query, conn)
    assert df.values[0][0] == len(full_dataset), f"{df.values[0][0]} does not equal"
    
    
# Create roadway attributes table

with engine.connect() as conn:

    try:
        conn.execute("DROP TABLE road_attrs;")
    except:
        print("The road_attrs table does not exist yet.")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS road_attrs
        ('osm_way_id' INT PRIMARY KEY NOT NULL,
        'road_name' VARCHAR(255),
        'road_type' VARCHAR(30),
        'one_way' VARCHAR(30),
        'surface' VARCHAR(30));
    """)

# Append roadway attributes dataframe to road_attrs sql table

with engine.connect() as conn:
    road_attrs.to_sql('road_attrs', conn, if_exists='append')
    
# Practice queries

with engine.connect() as conn:

    query = """ SELECT 
                    road_name, 
                    road_type, 
                    one_way, 
                    surface 
                FROM 
                    road_attrs 
                WHERE 
                    one_way 
                IS NOT NULL AND 
                    surface 
                IS NOT NULL;"""
                
    df = pd.read_sql(query, conn) 
df


with engine.connect() as conn:
    
    query = """ SELECT 
                    road_attrs.road_name,
                    avg(speeds.speed_kph_mean),
                    avg(speeds.speed_kph_p85)
                FROM 
                    road_attrs
                JOIN speeds ON
                    speeds.osm_way_id = road_attrs.osm_way_id
                GROUP BY
                    road_name,
                    hour_of_day
                ORDER BY
                    avg(speeds.speed_kph_mean) DESC;"""
    
    df = pd.read_sql(query, conn)
    
df

# A pre-requisite to this query is making seperate tables in sql for each quarter
# Note that a union "stacks" two tables vertically while a join combines two tables horizontally

with engine.connect() as conn:
    
    query = """ SELECT 
                    *
                FROM 
                    q1_speeds
                UNION
                SELECT 
                    *
                FROM
                    q2_speeds                
                UNION
                SELECT 
                    *
                FROM
                    q3_speeds
                UNION
                SELECT 
                    *
                FROM
                    q4_speeds;"""
    
    df = pd.read_sql(query, conn)
    
df
