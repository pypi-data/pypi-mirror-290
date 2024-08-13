import unittest
from pucktrick.outliers import * 
from pucktrick.duplicated import * 
import pandas as pd
from pandas.testing import assert_frame_equal

class Test_outlies(unittest.TestCase):
  
  def test_duplicateClassNew(self):
      percentage=0.5
      num_rows = 1000
      fake_df=create_fake_table(num_rows)
      target='f3'
      value='banana'
      old_len=len(fake_df[fake_df[target]==value])
      noise_df=duplicateClassNew(fake_df,target,value,percentage)
      #new_percentage=0.7
      #noise_df=duplicateAllExtended(fake_df,noise_df,new_percentage)
      new_len=len(noise_df[noise_df[target]==value])
      diff=round((new_len-old_len)/old_len,2)
      self.assertEqual(diff, percentage)
  
  def test_duplicateAllExtended(self):
      percentage=0.5
      num_rows = 1000
      fake_df=create_fake_table(num_rows)
      noise_df=duplicateAllNew(fake_df,percentage)
      new_percentage=0.7
      noise_df=duplicateAllExtended(fake_df,noise_df,new_percentage)
      new_len=len(noise_df)
      diff=(new_len-num_rows)/num_rows
      self.assertEqual(diff, new_percentage)


  def test_outliersCategoricalString(self):
        percentage=0.5
        num_rows = 1000
        fake_df=create_fake_table(num_rows)
        column='f3'
        noise_df=outlierCategoricalStringNew(fake_df,column,percentage)
        dif = fake_df[column] != noise_df[column]
        diff_number = dif.sum()
        percentage=0.7
        noise_df=outliercategoricalStringExtended(fake_df,noise_df,column,percentage)
        dif = fake_df[column] != noise_df[column]
        diff_number = dif.sum()
        diff_p=diff_number/num_rows
        self.assertEqual(diff_p, percentage)
  
  def test_outliersCategoricalInt(self):
        percentage=0.5
        num_rows = 1000
        fake_df=create_fake_table(num_rows)
        column='f1'
        noise_df=outlierCategoricalIntegerNew(fake_df,column,percentage)
        dif = fake_df[column] != noise_df[column]
        diff_number = dif.sum()
        percentage=0.7
        noise_df=outliercategoricalIntegerExtended(fake_df,noise_df,column,percentage)
        dif = fake_df[column] != noise_df[column]
        diff_number = dif.sum()
        diff_p=diff_number/num_rows
        self.assertEqual(diff_p, percentage)
  
  def test_outliersdiscrete(self):
        percentage=0.5
        num_rows = 1000
        fake_df=create_fake_table(num_rows)
        column='f1'
        noise_df=outlierDiscreteNew3Sigma(fake_df,column,percentage)
        dif = fake_df[column] != noise_df[column]
        diff_number = dif.sum()
        percentage=0.7
        noise_df=outlierDiscreteExtended3Sigma(fake_df,noise_df,column,percentage)
        dif = fake_df[column] != noise_df[column]
        diff_number = dif.sum()
        diff_p=diff_number/num_rows
        # Verifica che il numero di modifiche sia corretto
        self.assertEqual(diff_p, percentage)

    

def create_fake_table(num_rows=1000):
  # Generate data for each column
  f1 = np.random.uniform(-100, 100, num_rows)  # Continuous values between -100 and 100
  f2 = np.random.randint(-100, 101, num_rows)  # Discrete values between -100 and 100
  f3 = np.random.choice(['apple', 'banana', 'cherry'], num_rows)  # String values
  f4 = np.random.choice(['apple', 'banana', 'cherry'], num_rows)  # String values
  f5 = np.random.choice([0, 1], num_rows)  # Binary values (0 or 1)
  target = np.random.choice([0, 1], num_rows)  # Binary target (0 or 1)

  # Create the DataFrame
  df = pd.DataFrame({
    'f1': f1,
    'f2': f2,
    'f3': f3,
    'f4': f4,
    'f5': f5,
    'target': target
  })
  return df

if __name__ == "__main__":
    unittest.main()
