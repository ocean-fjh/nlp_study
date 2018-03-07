#-*- coding:utf-8 -*-

import os

from pyltp import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer
from pyltp import Parser
from pyltp import SementicRoleLabeller


class pyltp_worker(object):
    
    #初始化，创建实例，加载基础模型
    def __init__(self,model_path):
        self.LTP_MODEL_DIR = model_path
        self.segmentor = Segmentor()   #分词
        self.postagger = Postagger()  #词性标注
        self.recognizer = NamedEntityRecognizer()  #命名实体识别
        self.parser = Parser()  #依存句法分析
        self.load_model()
    
    #加载基础模型
    def load_model(self):
        self.cws_model_path = os.path.join(self.LTP_MODEL_DIR , 'cws.model')  #分词模型路径
        self.pos_model_path = os.path.join(self.LTP_MODEL_DIR , 'pos.model')  #词性标注模型路径   
        self.ner_model_path = os.path.join(self.LTP_MODEL_DIR , 'ner.model')  #命名实体识别模型路径
        self.par_model_path = os.path.join(self.LTP_MODEL_DIR , 'parser.model')  #依存句法分析模型路径
        self.segmentor.load(self.cws_model_path)  #加载cws模型
        self.postagger.load(self.pos_model_path)  #加载pos模型
        self.recognizer.load(self.ner_model_path)  #加载ner模型
        self.parser.load(self.par_model_path)  #加载parser模型
        
    #释放实例    
    def end(self):
        self.segmentor.release()  #分词
        self.postagger.release()  #词性标注
        self.recognizer.release()  #命名实体识别
        self.parser.release()  #依存句法分析
    
    #加入自定义词典
    
    def add_cws_userdict(self,lexicon_path):
        self.segmentor.load_with_lexicon(lexicon_path)
        
    def add_pos_userdict(self,lexicon_path):
        self.postagger.load_with_lexicon(lexicon_path) 
        
    def add_ner_userdict(self,lexicon_path):
        self.recognizer.load_with_lexicon(lexicon_path) 
        
    def add_par_userdict(self,lexicon_path):
        self.parser.load_with_lexicon(lexicon_path)  
    
    #分句。按照标点符号来分，返回句子列表。
    def sentsplit(self,text):
        sentences = SentenceSpliter.split(text)
        sentences_list=list(sentences)
        return sentences_list

    #分词。返回词列表。
    def cws(self,text):
        words = self.segmentor.segment(text)
        words_list = list(words)
        return words_list

    #词性标注。返回词性标注列表。
    def pos(self,words):
        postags = self.postagger.postag(words)
        postags_list = list(postags)
        return postags_list

    #命名实体识别。返回命名实体类型列表。
    def ner(self,words,postags):
        nertags = self.recognizer.recognize(words,postags)
        nertags_list = list(nertags)
        return nertags_list
    

    #依存句法分析。
    def par(self,words,postags):
        arcs = self.parser.parse(words,postags)
        pr_list=[]
        word_list=[]
        word_pos_list=[]
        source_list=[]
        source_pos_list=[]
        relation_list=[]
        for i,k in enumerate(arcs):
            word = words[i]
            word_pos = postags[i]
            source = words[k.head-1]
            source_pos = postags[k.head-1]
            relation = k.relation
            word_list.append(word)
            word_pos_list.append(word_pos)
            source_list.append(source)
            source_pos_list.append(source_pos)
            relation_list.append(relation)
            pr_list.append([word,word_pos,source,source_pos,relation])
        df_list=[word_list,word_pos_list,source_list,source_pos_list,relation_list]
        return  pr_list,df_list,arcs

worker = pyltp_worker('../dp_relation/dp_relation/ltp_data')   
words = worker.cws('小明喜欢小芳')
postags = worker.pos(words)
arcs = worker.par(words,postags)[0]

print('分词','\t','词性','\t','关联词','\t','词性','\t','关系')
print('-'*36)
for i in arcs:
    print(i[0],'\t',i[1],'\t',i[2],'\t',i[3],'\t',i[4])

worker.end()