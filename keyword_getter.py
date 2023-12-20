import pandas as pd
import langid



def keyword_get():
    keyword_file = pd.read_excel('캠페인별 키워드 performance.xlsx')
    keyword_file['keyword'] = keyword_file['keyword'].str.replace(' ','')
    keyword_file['keyword'] = keyword_file['keyword'].replace(to_replace=r'\d{'+str(3)+r',}', value='', regex=True)
    keyword_file = keyword_file[['keyword','전환금액','투자금액', 'campaign']].groupby(['keyword']).sum().reset_index()
    keyword_file['ROAS'] = keyword_file['전환금액']/keyword_file['투자금액']
    
    keyword_df = keyword_file[['keyword', 'ROAS', 'campaign']]
    keyword_df = keyword_df.sort_values(by=['ROAS'])
    print('pruned keyword = ')
    print(keyword_df)
    return keyword_df
    

if __name__=='__main__':
    keyword_get()