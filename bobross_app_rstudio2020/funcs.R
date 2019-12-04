title_word <- function(w){
  if (w == "sunset"){w <- "sun"}
  bob <- read.csv("data/bob-ross.csv")
  w <- toupper(w)
  
  bob <- bob[bob[[w]] == 1, c("TITLE", w)]
  
  stopWords <- toupper(stopwords())
  vec <- removeWords(gsub("\"", "", paste(bob[bob[[w]] == 1,]$TITLE, collapse = ' ')), stopWords)
  vec <- gsub("---", " ", gsub(" & ", "", trimws(gsub("  ", " ", gsub("   ", " ", vec)))))
  words <- strsplit(vec, " ")[[1]]
  acqTag <- tagPOS(tolower(words))
  words_tagged <- strsplit(acqTag$POStagged, " ")[[1]]
  
  nouns <- c()
  adjs <- c()
  for (word in words_tagged) {
    if (str_sub(word, -3, -1) == "/NN") {
      nouns <- c(nouns, word)
    }
    if (str_sub(word, -3, -1) == "/JJ") {
      adjs <- c(adjs, word)
    } 
  }
  
  toupper(paste(str_sub(sample(adjs, 1), 1, -4), str_sub(sample(nouns, 1), 1, -4)))
}

tagPOS <-  function(x, ...) {
  s <- as.String(x)
  word_token_annotator <- Maxent_Word_Token_Annotator()
  a2 <- Annotation(1L, "sentence", 1L, nchar(s))
  a2 <- NLP::annotate(s, word_token_annotator, a2)
  a3 <- NLP::annotate(s, Maxent_POS_Tag_Annotator(), a2)
  a3w <- a3[a3$type == "word"]
  POStags <- unlist(lapply(a3w$features, `[[`, "POS"))
  POStagged <- paste(sprintf("%s/%s", s[a3w], POStags), collapse = " ")
  list(POStagged = POStagged, POStags = POStags)
}

run_apriori <- function(word) {
  bob <- read.csv("data/data.csv")[c(3:61)]
  bob2 <-apply(bob,2,as.logical)
  bob3 <- as(bob2, "transactions")
  rules <- apriori(data=bob3,parameter=list(minlen=2,conf=0.35), appearance=list(default="rhs",lhs=word), control=list(verbose=F))
  rules_conf <- sort(rules, by="confidence", decreasing=TRUE) 
  answers <- rep(" ",1)
  if (length(rules_conf)>0) {
    x <- DATAFRAME(rules_conf)$RHS
    y <- unique(x)
    answers <- rep(NA, length(y))
    ind =1
    for (val in y) {
      answers[ind]=str_remove_all(val, "[{}]")
      ind = ind +1
    }
  }
  answers
}

surprise <- function() {
  bob <- read.csv("data/data.csv")[c(1:2)]
  ind <- sample(1:nrow(bob), 1)
  ans<- paste(bob[ind,1], ": \"", str_remove_all(bob[ind,2], "\""),"\"",sep="")
  ans
}

my_knn <- function(v1,v2){
  col1 <- read.csv("data/col1.csv")
  newdf <- col1[3:18]
  my_l <- colnames((newdf))
  newrow = rep(0,16)
  sel <- c(v1,v2)
  for (x in sel){
    i <- which(x == my_l)[[1]]
    newrow[i] = 1
  }
  new <- knn(newdf, newrow, seq(1,nrow(col1)), k = 1)
  ans <- paste(col1[new,1], ": \"", str_remove_all(col1[new,2], "\""),"\"",sep="")
  ans
}

special <- function(v1){
  col2 <- read.csv("data/col2.csv")
  newdf <- col2[ which(col2[v1] >0), ]
  ind <- sample(as.numeric(rownames(newdf)), 1)
  ans<- paste(col2[ind,1], ": \"", str_remove_all(col2[ind,2], "\""),"\"",sep="")
  ans
}
