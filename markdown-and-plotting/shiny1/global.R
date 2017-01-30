library(shiny)
library(ggplot2)

setwd('~/Documents/bigValley-Python')
files <- grep('.csv$', list.files('testData'), value=TRUE)

loadBigOnes <- function(folder) {
  # get files
  files <- grep('.csv$', list.files(folder), value=TRUE)
  # seperate out the ones that end in a 5000 run
  bigOnes <- list()
  for (file in files) {
    # load a file
    thisOne <- read.csv(paste(folder,file,sep='/'))
    if (max(thisOne[,2], na.rm = T) == 5000) {
      names(thisOne) <- c("tests", "maxYears",
                          "firstExt","firstExtStd","deadWorld", "deadWorldStd", "id",
                          "wolfEn", "wolfRe", "wolfFa", "rabbitEn", "rabbitRe", "rabbitFa",
                          "wolfNum", "rabbitNum", "grassNum", "rockNum")
      #
      model <- unlist(strsplit(file, "-"))[2]
      id <- gsub('\\.csv', '', unlist(strsplit(file, "-"))[3])
      thisOne$model = rep(model,nrow(thisOne))
      thisOne$id = rep(id,nrow(thisOne))
      thisOne$iteration <- as.numeric(row.names(thisOne))
      #
      bigOnes[[length(bigOnes) + 1]] <- thisOne
    }
  }
  print(paste(length(bigOnes), 'bigOnes'))
  return(bigOnes)
}

bigOnes <- loadBigOnes('testData')

########
oneBig <- data.frame()
for (df in bigOnes) {
  oneBig <- rbind(oneBig, df)
}
#######
ends <- oneBig[oneBig$maxYears==5000 & !is.na(oneBig$maxYears), ]
df <- oneBig


###### http://www.ats.ucla.edu/stat/r/faq/reshape.htm

##
full <- list()
critters <- list()
numbers <- list()

for (id in ends$id) {
  l <- reshape(df[df$id==id, 8:19], 
               varying = c("wolfEn", "wolfRe", "wolfFa", "rabbitEn", "rabbitRe", "rabbitFa",
                           "wolfNum", "rabbitNum", "grassNum", "rockNum"), 
               v.names = "number",
               timevar = c("stat"), 
               times = c("wolfEn", "wolfRe", "wolfFa", "rabbitEn", "rabbitRe", "rabbitFa",
                         "wolfNum", "rabbitNum", "grassNum", "rockNum"), 
               new.row.names = NULL,
               direction = "long")
  
  ln <- l[grep('Num', l$stat),]
  lc <- l[grep('En|Re|Fa', l$stat),]
  print(head(l))
  full[[length(full) + 1]] <- ggplot(l, aes(x=iteration, y=number, colour=stat)) + geom_line() + xlim(400,max(l$iteration)) + ggtitle(paste(id, "-", l$model[1]))
  numbers[[length(numbers) + 1]] <- ggplot(ln, aes(x=iteration, y=number, colour=stat)) + geom_line() + xlim(400,max(l$iteration)) + ggtitle(paste(id, "-", l$model[1]))
  critters[[length(critters) + 1]] <- ggplot(lc, aes(x=iteration, y=number, colour=stat)) + geom_line() + xlim(400,max(l$iteration)) + ggtitle(paste(id, "-", l$model[1]))
}

plots <- function(pick = 'full', sleep = 3) { #'full' 'critters' or 'numbers'
  if (pick == 'full') {
    for (plot in full) {
      suppressWarnings(print(plot))
      Sys.sleep(sleep)
    }
  } else if (pick == 'critters') {
    for (plot in critters) {
      suppressWarnings(print(plot))
      Sys.sleep(sleep)
    }
  } else if (pick == 'numbers') {
    for (plot in numbers) {
      suppressWarnings(print(plot))
      Sys.sleep(sleep)
    }
  } else {
    print("INVALIDED PICK: only 'full' 'critters' or 'numbers'")
  }
  print("%%%%%%%%% all done. %%%%%%%%%")
}