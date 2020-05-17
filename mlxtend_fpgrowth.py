# dataset = [['Milk', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
#            ['Dill', 'Onion', 'Nutmeg', 'Kidney Beans', 'Eggs', 'Yogurt'],
#            ['Milk', 'Apple', 'Kidney Beans', 'Eggs'],
#            ['Milk', 'Unicorn', 'Corn', 'Kidney Beans', 'Yogurt'],
#            ['Corn', 'Onion', 'Onion', 'Kidney Beans', 'Ice cream', 'Eggs']]

dataset = [['I1', 'I2', 'I5'],
            ['I2', 'I4'],
            ['I2', 'I3'],
            ['I1', 'I2', 'I4'],
            ['I1', 'I3'],
            ['I2', 'I3'],
            ['I1', 'I3'],
            ['I1', 'I2', 'I3', 'I5'],
            ['I1', 'I2', 'I3']]

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder

te = TransactionEncoder()
te_ary = te.fit(dataset).transform(dataset)
df = pd.DataFrame(te_ary, columns=te.columns_)
print(df)

from mlxtend.frequent_patterns import fpgrowth

print(fpgrowth(df, min_support=0.1))

print(fpgrowth(df, min_support=0.1, use_colnames=True))