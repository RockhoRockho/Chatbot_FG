import pandas as pd
import numpy as np
import os

def NerPreProcess(intentNumber, tagName):
    
    # ner_tag 데이터 준비
    df = pd.read_csv('ner_tag.csv', header=None) 
    df.columns = ['word', 'tag', 'intent']

    # 문장데이터 준비
    sent_df = pd.read_csv('D:/github/Chatbot_FG/models/intent/Intent_train_data.csv', header=None) 
    sent_df.columns = ['sentence', 'intent', 'intent_info']
    
    # 첫번째 문장 준비 (아무것도 없는 문장 [';'←붙이기 전])
    sent0 = []
    for sentence in sent_df[sent_df['intent'] == intentNumber]['sentence'].unique():
            sent0.append(sentence)

    # 두번째 문장 준비
    sent0_2 = sent0 # sent0 문장가져오기
    sent0_3 = []    # 두번째 문장틀
    for sent in sent0:
        for intent_word in df[df['intent'] == intentNumber]['word']:
            if sent.replace(intent_word, f'$<{intent_word}:{tagName}>') not in sent0_3: # 이미 태깅된거 있다면 거른다.
                if sent.find(intent_word) >= 0:
                    sent0_3.append(sent.replace(intent_word, f'<{intent_word}:{tagName}>')) # 사전에 있는건 태깅 replace
                    break # 똑같은 문장에 다른 태깅 추가 방지

    # 맨앞 '$' 붙이기
    for idx, sent in enumerate(sent0_3):
        sent0_3[idx] = '$' + sent

    # 세번째 문단 준비
    # 전처리
    from utils.Preprocess import Preprocess
    p = Preprocess(word2index_dic=os.path.join('./train_tools/dict', 'chatbot_dict.bin'),
                   userdic=os.path.join('./utils', 'train.tsv'))
    # 형태소 분석
    sequences = []
    for sentence in sent0:
        pos = p.pos(sentence)
        sequences.append(pos)

    # 첫번째 문장 수정(아무것도 없는 문장 [';'←붙인 후])
    sent0 = []
    for sentence in sent_df[sent_df['intent'] == intentNumber]['sentence'].unique():
            sent0.append('; ' + sentence)

    # concat 위해 Dataframe 열 맞추기 / column[0] -> index 로 만들어버리기
    s_df1 = pd.DataFrame(sent0) 
    s_df1[1] = np.nan
    s_df1['tag'] = np.nan
    s_df1.set_index(0, inplace=True)
    s_df1[0] = np.nan

    s_df2 = pd.DataFrame(sent0_3)
    s_df2[1] = np.nan
    s_df2['tag'] = np.nan
    s_df2.set_index(0, inplace=True)
    s_df2[0] = np.nan

    # result_df
    result_df = pd.DataFrame({0:[np.nan], 1:[np.nan], 'tag':[np.nan]})

    # ENTER 할 빈 Dataframe 만듦
    pos_df_zero = pd.DataFrame({0:[np.nan], 1:[np.nan], 'tag':[np.nan]})
    pos_df_zero.set_index(0, inplace=True)
    pos_df_zero[0] = np.nan
    
    # 사전만들기
    dic = df[df['tag'] == tagName]['word'].tolist()

    for s_idx, sent in enumerate(sequences):
        pos = []
        result_df = pd.concat([result_df, pd.DataFrame(s_df1.iloc[s_idx]).transpose(), pd.DataFrame(s_df2.iloc[s_idx]).transpose()]) # 처음 문장과, 태깅추가된 문장추가
        for i in range(len(sent)):
            pos.append(list(sent[i])) # 튜플 -> 리스트
            pos_df = pd.DataFrame(pos)
            pos_df['tag'] = 'O'
            for p_idx, p in enumerate(pos_df[0]):
                if p in dic:
                    pos_df['tag'][p_idx] = 'B_' + tagName # ner_tag 사전에 포함된 단어 BIO 태깅
                    pos_df.reset_index(inplace=True)
                    pos_df.index += 1 # index 번호 1부터
        result_df = pd.concat([result_df, pos_df, pos_df_zero]) # ENTER 하기

    return result_df[[0, 1, 'tag']] # 필요한 열만 출력