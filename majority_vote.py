import pandas as pd
import numpy as np

def generate_majority_dict(path):
    """
    return all the tags and counts
    """
    infile = pd.read_csv(path)

    majority = {}
    for i, row in infile.iterrows():
        j = 2
        while row[j] != '\r\n' and row[j] != '':
            if row[j] in majority:
                majority[row[j]] += 1
            else:
                majority[row[j]] = 1
                
            j+=1
    majority_df = pd.DataFrame.from_dict(majority, orient='index')
    majority_df.to_csv('majority_file.csv')
    majority = pd.read_csv('majority_file.csv')
    majority.columns = ['words','counts']
    return majority


def load_entity_sets(m):
    """
    load the multi word entities and their 
    different annotations
    """
    entity = {}
    for i in range(len(m)):
        tag, count = m.at[i, 'words'], m.at[i, 'counts']
        text = tag.split('$')
        query = ""
        for k in range(len(text)):
            if k%2 == 0:
                query += text[k] + ' '
        
        query = query.replace(' ', '_').rstrip('_')
        
        if query in entity:
            if tag in entity[query]:
                continue
            else:            
                entity[query][tag] = count
        else:
            entity[query] = {tag: count}
            
    #entity = pd.DataFrame(entity)
    return entity

def get_sentence_ids(path):
    """
    get list of sentence ids for each
    tagged annotation terms/relationships
    """
    
    entity_to_sentid = {}
    df = pd.read_csv(path)
    for i in range(len(df)):
        j = 2
        term = df.at[i, str(j)]
        print(term)
        if term != '\r\n' and term != '':
            if term in entity_to_sentid:
                entity_to_sentid[term].append(df.at[i, '0'])
            else:
                entity_to_sentid[term] = [df.at[i, '0']]
        j += 1
    
    return entity_to_sentid

                
if __name__ == "__main__":
    
    df = []
    with open('AnnotatedData.tsv', 'r', encoding='utf8') as infile:
        for row in infile:
            text = row.split('\t')
            df.append(text)
        df = pd.DataFrame(df)

    df = df.apply(lambda x: x.astype(str).str.lower())
    df = df[df[2] != '\n'].reset_index(drop=True)
    df = df.apply(lambda x: x.replace('none',''))
    df.to_csv('annotated_lower_removed.csv', index=False)
    path = 'annotated_lower_removed.csv'
    majority = generate_majority_dict()
    entities = load_entity_sets(majority)
    entities_with_sentid = get_sentence_ids(path)
            
    
    
