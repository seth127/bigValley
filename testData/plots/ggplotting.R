setwd('/Users/Seth/Documents/bigValley/testData')

library(ggplot2)

cols = c('tests','years','firstExt', 'firstExtSTD', 'deadWorld', 'deadWorldSTD', 'id',
         'wolfEn',
         'wolfRe',
         'wolfFa',
         'rabbitEn',
         'rabbitRe',
         'rabbitFa',
         'wolfNum',
         'rabbitNum',
         'grassNum',
         'debrisNum', 'pred')

df1 <- read.csv('1x500SIMS-RF1.csv', stringsAsFactors = F, col.names = cols, header = F)
df1$iteration <- as.numeric(row.names(df1))
View(df1)

df3 <- read.csv('3x500SIMS-RF1.csv', stringsAsFactors = F, quote="'", col.names = cols, header = F)
df3$iteration <- as.numeric(row.names(df3))
View(df3)

###### 1x500
reg1 <- lm(firstExt ~ iteration, data = df1)

g <- ggplot(df1, aes(x=iteration, y=firstExt)) + geom_point() + ggtitle('1x500')
g <- g + geom_abline(intercept = reg1$coefficients[1], slope = reg1$coefficients[2], color = "red")
g + geom_smooth(formula = firstExt ~ iteration)

###### 3x500
reg3 <- lm(firstExt ~ iteration, data = df3)

g <- ggplot(df3, aes(x=iteration, y=firstExt)) + geom_point() + ggtitle('3x500')
g <- g + geom_abline(intercept = reg3$coefficients[1], slope = reg3$coefficients[2], color = "red")
g + geom_smooth(formula = firstExt ~ iteration)


########
########
library(kernlab)




library(randomForest)
