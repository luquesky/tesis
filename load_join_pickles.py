import pickle
from tqdm import tqdm

def merge_two_dicts(x, y):
        z = x.copy()   # start with x's keys and values
        z.update(y)    # modifies z with y's keys and values & returns None
        return z


merged_data = {}
filename = 'list_of_pkls_all.lst'
with open(filename,'r') as stream:
    for line in tqdm(stream):
    #for line in stream:
        data_file = line.strip().split()
        with open(''.join(data_file),'rb') as stream:
            data = pickle.load(stream)
            merged_data = merge_two_dicts(merged_data,data)

pickle.dump(  merged_data , open( "all_pkl_data.pkl", "wb" ) )
