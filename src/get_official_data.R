library(tidyverse)

setwd('~/Desktop/instagram_get_followers/src/')
data = read_csv('../data/data.csv')

data_man <- 
  data %>% 
  filter(str_detect(NumberOfFollowers, "万"))

data_more_than_sen <- 
  data %>% 
  filter(!str_detect(NumberOfFollowers, "万")) %>% 
  mutate(
    'NumberOfFollowers_int' = NumberOfFollowers %>% as.integer() 
  ) %>% 
  filter(NumberOfFollowers_int >= 1000) %>% 
  select(!NumberOfFollowers_int)

data_official <- 
  data_man %>% 
  bind_rows(data_more_than_sen) %>% 
  write_csv('../data/data_official.csv')
