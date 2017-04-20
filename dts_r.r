library(caret)
library(ggfortify)
library(rpart)
library(rpart.plot)
library(RSQLite)
library(DBI)
library(randomForest)

get_nn = function(d, point, k){
  point = d[point, ]
  dists = sort(sqrt(rowSums((t(t(d) - point))^2)))
  close_points = names(dists)[1:k]
  return(close_points)
}

base_dir<- "C:/Users/Jeff/Documents/research/Sadler_3rdPaper/manuscript/"
data_dir<- paste(base_dir, "Data/", sep="")
fig_dir <- paste(base_dir, "Figures/general/", sep="")
db_filename <- "floodData.sqlite"
print(paste(data_dir, db_filename))
con = dbConnect(RSQLite::SQLite(), dbname=paste(data_dir, db_filename, sep=""))

dbListTables(con)

df = dbReadTable(con, 'for_model')
df = subset(df, rain_daily_sum>0.1) # only look at days that have over 0.1 in of rainfall
df = df[!is.na(df$gw_daily_avg),] # remove null gw values
short_names = c('rd', 'rhr', 'rhmxtime', 'r15', 'r15mxtime', 'r3d', 'gw', 'td', 'tr15mx', 'trhrmx', 'wdd', 'wvd',  'wvh', 'nfld', 'fld', 'evnme', 'evdte')
colnames(df) = short_names

in_col_names = c('rd', 'rhr', 'r15', 'r3d', 'gw', 'td', 'tr15mx', 'trhrmx', 'wvd')
out_col_name = 'fld'
data = df[, c(in_col_names, out_col_name)]
#data$fld = df$fld>0

fmla = as.formula(paste(out_col_name, "~", paste(in_col_names, collapse="+")))

fit = rpart(fmla, method='class', data=data, minsplit=7)

tiff(paste(fig_dir, "Plot2.tif"), width=9, height=6, units='in', res = 300)
rpart.plot(fit, under=TRUE, cex=0.9, extra=1, varlen = 6)
dev.off()
rpart.plot(fit, under=TRUE, cex=0.9, extra=1, varlen = 6)

# pca
data = data.frame(scale(data))
pca = prcomp(data)
p = ggplot(pca$x[,c(1,2)], aes(x=PC1, y=PC2, colour=data[, out_col_name], label=rownames(pca$x)))
p + geom_point() +geom_text()
point = "2"
neighs = get_nn(pca$x, point, 5)
data[neighs,]

# creating predictive model
data$fld = factor(data$fld)
prt = createDataPartition(data$fld, p=0.7)
train_ind = prt$Resample1
forest = randomForest(fmla, data = data, importance = TRUE, type="classification")

# check on training data
pred = predict(forest, data[train_ind, in_col_names])
true_fld = data[train_ind, 'fld']
print(sum(pred == true_fld)/length(true_fld))

# check on testing data
pred = predict(forest, data[-train_ind, in_col_names])
true_fld = data[-train_ind, 'fld']
print(sum(pred == true_fld)/length(true_fld))

