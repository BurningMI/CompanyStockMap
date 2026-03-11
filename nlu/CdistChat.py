from NLUConfig import NLUConfig
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import sklearn
import numpy as np

class CdistChat:

    def __init__(self, conf):
        self.conf = conf
        self.data_path = conf.train_data_path

      
    def load_data(self, rand_seed=998):                         #加载意图判断数据,随机种子默认998

        self.X, self.y = [], []
        with open(self.data_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
              if not line.strip():
                  continue
              parts = line.strip().split(",")
              text, label = ",".join(parts[:-1]), parts[-1]
              text = " ".join(list(text))
              self.X.append(text)
              self.y.append(label)

        # 打乱数据
        self.X, self.y = shuffle(
            self.X, self.y, random_state=rand_seed
        )
        
        #print(f"labeltype:{set(self.labels)}")
        return self.X, self.y
      
      
    def run(self):
        # 加载数据
        X, y = self.load_data()
        labels_type = set(y)
        labels_type2id = {label: idx for idx, label in enumerate(labels_type)}
        id2labels_type = {idx: label for label, idx in labels_type2id.items()}
        
        
        # print(f"labeltype2id:{labels_type2id}")
        # print(f"id2labeltype:{id2labels_type}")
        
        y=[labels_type2id[i] for i in y]   #将标签转换为数字id 此时的labels是一个数字列表，内容是每个文本对应的标签id
        
        labels_name=sorted(labels_type2id.items(), key = lambda kv:kv[1], reverse=False)
        
        targert_names=[i[0] for i in labels_name]
        #得到标签名称和标签id的列表，按照标签id升序排列
        
        # print(f"targert_names:{targert_names}")
        # print(f"targert_labels:{targert_labels}")
        
        train_X, test_X, train_y, test_y = train_test_split(self.X, y, test_size=0.2, random_state=42)
        
        
        vec = TfidfVectorizer(ngram_range=(1,3), min_df=0.0, max_df=0.9, analyzer='char') #转换成TF-IDF特征，使用1-3元字符特征，过滤掉在所有文本中出现频率过高或过低的特征
        
        

        train_X = vec.fit_transform(train_X)
        test_X = vec.transform(test_X)
        
        
        #----------------------------逻辑回归模型----------------------------

        LR=LogisticRegression(C=8, solver='lbfgs', max_iter=1000)
        LR.fit(train_X, train_y)
        
        #lr_preds=LR.predict(test_X)    #直接出结果
        lr_preds_proba=LR.predict_proba(test_X)  #得到每个类别的概率分布
        
        # print(f'preds--》{lr_preds}')
        # print(classification_report(test_y, lr_preds, target_names=targert_names))
        # print(confusion_matrix(test_y, lr_preds, labels=targert_names))

        #----------------------------GBTD模型----------------------------
        GBDT=sklearn.ensemble.GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)
        GBDT.fit(train_X, train_y)
        #gbdt_preds=GBDT.predict(test_X)
        gbdt_preds_proba=GBDT.predict_proba(test_X)
        # print(f'gbdt_preds--》{gbdt_preds}')
        # print(classification_report(test_y, gbdt_preds, target_names=targert_names))
        # print(confusion_matrix(test_y, gbdt_preds, labels=targert_names))
      
        #----------------------------模型融合---------------------------

        final_pred = np.argmax((lr_preds_proba+gbdt_preds_proba)/2, axis=1)

        
        print(classification_report(test_y, final_pred, target_names=targert_names))
        print(confusion_matrix(test_y, final_pred))


      
      

    


if __name__ == "__main__":
    nc = NLUConfig()
    cc = CdistChat(nc)
    # cc.load_data()
    cc.run()
   
    #print(cc.load_data()) 
