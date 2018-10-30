import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tkinter

df = pd.DataFrame(data=np.random.randn(10, 4).cumsum(0),
                  columns = ['A', 'B', 'C', 'D'],
                  index = np.arange(0, 100, 10)
                  )

df.plot.line()
plt.show()