
repo = "http://cran.us.r-project.org"
library(caret)
library(ggfortify)
library(rpart)
library(rpart.plot)
library(RSQLite)
library(DBI)
library(randomForest)
library(e1071)
library(class)

classify_knn = function(pca.data, obs_data, point, k){
  neighs = get_nn(pca.data, point, k)
  neigh_data = obs_data[neighs,]
  return(names(which.max(table(neigh_data$fld))))
}

get_nn = function(d, point, k){
  point = d[point, ]
  dists = sort(sqrt(rowSums((t(t(d) - point))^2)))
  close_points = names(dists)[2:k]
  return(close_points)
}

base_dir<- "C:/Users/Jeff/Documents/research/Sadler_3rdPaper/manuscript/"
data_dir<- paste(base_dir, "Data/", sep="")
fig_dir <- paste(base_dir, "Figures/general/", sep="")
db_filename <- "floodData.sqlite"

con = dbConnect(RSQLite::SQLite(), dbname=paste(data_dir, db_filename, sep=""))

df = dbReadTable(con, 'for_model')
df = subset(df, rain_daily_sum>0.1) # only look at days that have over 0.1 in of rainfall
df = df[!is.na(df$gw_daily_avg),] # remove null gw values
short_names = c('rd', 'rhr', 'rhmxtime', 'r15', 'r15mxtime', 'r3d', 'gw', 'td', 'tr15mx', 'trhrmx', 'wdd', 'wvd',  'wvh', 'nfld', 'fld', 'evnme', 'evdte')
colnames(df) = short_names

in_col_names = c('rd', 'rhr', 'r15', 'r3d', 'gw', 'td', 'wvd', 'tr15mx', 'trhrmx')
out_col_name = 'fld'
model_data = df[, c(in_col_names, out_col_name)]
model_data$fld = df$fld>0
model_data$fld = factor(model_data$fld)

prt = createDataPartition(model_data$fld, p=0.7)
train_ind = prt$Resample1

train_in_data = model_data[train_ind, in_col_names]
test_in_data = model_data[-train_ind, in_col_names]

train_col_stds = apply(train_in_data, 2, sd)
train_col_means = colMeans(train_in_data)

train_normalized = t((t(train_in_data)-train_col_means)/train_col_stds)
test_normalized = t((t(test_in_data)-train_col_means)/train_col_stds)

pca = prcomp(train_normalized)
pca$x = -pca$x
pca$rotation=-pca$rotation
p = ggplot(pca$x[,c(1,2)], aes(x=PC1, y=PC2, colour=model_data[train_ind, out_col_name], label=rownames(pca$x)))
p + geom_point() + geom_text()
plot(pca)
print(pca)

trn_preprocessed = predict(pca, train_normalized)
tst_preprocessed = predict(pca, test_normalized)
trn_in = trn_preprocessed
tst_in = tst_preprocessed

tst_out = model_data[-train_ind, 'fld']
trn_out = model_data[train_ind, 'fld']
train_data = cbind(as.data.frame(trn_in), fld = model_data[train_ind, 'fld'])
fmla = as.formula(paste(out_col_name, "~", paste(colnames(trn_in), collapse="+")))
fmla

kfit = knn(trn_in, tst_in, trn_out, k=5)
table(tst_out, kfit)

svm_fit = svm(fmla, data=train_data)
svm_pred = predict(svm_fit, tst_in)
table(tst_out, svm_pred)

dt_fmla = as.formula(paste(out_col_name, "~", paste(in_col_names, collapse="+")))
dt_train_data = model_data[train_ind, ]
dt_test_data = model_data[-train_ind, in_col_names]

fit = rpart(dt_fmla, method='class', data=dt_train_data, minsplit=2)
printcp(fit)

tiff(paste(fig_dir, "Plot2.tif"), width=9, height=6, units='in', res = 300)
rpart.plot(fit, under=TRUE, cex=0.9, extra=1, varlen = 6)
dev.off()
rpart.plot(fit, under=TRUE, cex=0.9, extra=1, varlen = 6)

pfit<- prune(fit, cp=fit$cptable[which.min(fit$cptable[,"xerror"]),"CP"])
rpart.plot(pfit, under=TRUE, cex=0.9, extra=1, varlen = 6)

pred = predict(pfit, dt_train_data[, in_col_names], type = 'class')
table(trn_out, pred)

pred = predict(pfit, dt_test_data, type = 'class')
table(tst_out, pred)

forest = randomForest(fmla, data = train_data, importance = TRUE, type="classification", nodesize=2)

pred = predict(forest, trn_in)
table(trn_out, pred)

pred = predict(forest, tst_in)
table(tst_out, pred)
forest$importance

lo_fit = glm(fmla, family=binomial(link='logit'), data=train_data)
print(lo_fit)

pred = predict(lo_fit, as.data.frame(tst_in), type="response")
table(tst_out, round(pred)>0)


