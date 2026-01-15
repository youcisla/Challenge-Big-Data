import plotly.express as px
import pandas as pd
import json

def test_serialization():
    print("--- Testing Pie Chart Serialization ---")
    data = {'Or': 394, 'Argent': 415, 'Bronze': 506}
    vals = [float(v) for v in data.values()]
    
    import json
    import plotly.utils
    
    # explicit list
    vals_list = [float(v) for v in data.values()]
    
    fig = px.pie(
        names=list(data.keys()),
        values=vals_list,
        title="Test Pie"
    )
    # FORCE LIST explicitly in trace
    fig.data[0]['values'] = vals_list
    
    # Method: to_dict -> json.dumps
    fig_dict = fig.to_dict()
    # Check if 'values' is now a list or bdata
    # Use standard json dumps to fail if it's numpy/bdata
    json_str_clean = json.dumps(fig_dict)
    
    parsed = json.loads(json_str_clean)
    print(f"Pie Values in Clean JSON: {parsed['data'][0]['values']}")
    
    print("\n--- Testing Map Serialization ---")
    df_data = [
        {'country_3_letter_code': 'USA', 'total_medals': 4657.0},
        {'country_3_letter_code': 'FRA', 'total_medals': 1315.0}
    ]
    df = pd.DataFrame(df_data)
    
    map_fig = px.choropleth(
        df,
        locations="country_3_letter_code",
        locationmode="ISO-3",
        color="total_medals",
        title="Test Map"
    )
    # FORCE LIST for Z
    map_fig.data[0]['z'] = df['total_medals'].tolist()
    
    map_dict = map_fig.to_dict()
    map_json_str_clean = json.dumps(map_dict)
    
    map_parsed = json.loads(map_json_str_clean)
    print(f"Map Z Values in Clean JSON: {map_parsed['data'][0]['z']}")

if __name__ == "__main__":
    test_serialization()
