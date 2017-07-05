
repo = "http://cran.us.r-project.org"
library(caret)
library(ggfortify)
library(ggplot2)
library(dplyr)
library(RSQLite)
library(DBI)
library(class)
library(pscl)
library(randomForest)

remove_cols= function(l, cols){
    return(l[! l %in% cols])
}

base_dir<- "C:/Users/Jeff/Documents/research/Sadler_3rdPaper/manuscript/"
data_dir<- "C:/Users/Jeff/Google Drive/research/Sadler_3rdPaper_Data/"
fig_dir <- paste(base_dir, "Figures/general/", sep="")
db_filename <- "floodData.sqlite"

con = dbConnect(RSQLite::SQLite(), dbname=paste(data_dir, db_filename, sep=""))

df = dbReadTable(con, 'for_model_avgs')

colnames(df)


cols_to_remove = c('event_name', 'event_date', 'num_flooded')
in_col_names = remove_cols(colnames(df), cols_to_remove)
# in_col_names = c('td_av', 'llt')
out_col_name = 'num_flooded'

model_data = df[, append(in_col_names, out_col_name)]
model_data = na.omit(model_data)
model_data = model_data[model_data[,'rd']>0.01,]

all_pred_tst = c()
all_pred_trn = c()
all_tst = c()
all_trn = c()
model_type = 'rf'
for (i in 1:100){
  print(paste("run: ", i, sep = ''))
  prt = createDataPartition(model_data[, out_col_name], p=0.7)
  
  train_data = model_data
  train_in_data = model_data[, in_col_names]
  train_out_data = model_data[, out_col_name]
  test_in_data = model_data[-prt$Resample1, in_col_names]
  test_out_data = model_data[-prt$Resample1, out_col_name]
  
  fmla = as.formula(paste(out_col_name, "~", paste(in_col_names, collapse="+")))

  if (model_type == 'poisson'){
	train_col_stds = apply(train_in_data, 2, sd)
	train_col_means = colMeans(train_in_data)

	train_normalized = t((t(train_in_data)-train_col_means)/train_col_stds)
	test_normalized = t((t(test_in_data)-train_col_means)/train_col_stds)

	pca = prcomp(train_normalized)

	trn_preprocessed = predict(pca, train_normalized)
	tst_preprocessed = predict(pca, test_normalized)

	fmla = as.formula(paste(out_col_name, "~", paste(colnames(trn_preprocessed), collapse="+")))

	train_data = cbind(as.data.frame(trn_preprocessed), num_flooded = model_data[prt$Resample1, out_col_name])
	train_in_data = trn_preprocessed
	test_in_data = tst_preprocessed

	output = glm(fmla, data=train_data, family = poisson)
  }
  else if (model_type == 'rf'){
	output = randomForest(fmla, data=train_data, importance = TRUE)
	impo = as.data.frame(output$importance)
	if (i == 1){
	  impo_df = data.frame(impo[,1])
	}
	else{
	  impo_df = cbind(impo_df, impo[,1])
	}
  }
  else if (model_type == 'zeroinf'){
	output = zeroinfl(fmla, data=train_data, importance = TRUE)
  }
  
  train_fld = train_out_data[train_out_data>0]
  pred_trn = predict(output, newdata = as.data.frame(train_in_data), type='response')
  pred_trn_capped = replace(pred_trn, pred_trn > 159, 159)
  pred_trn_fld = pred_trn_capped[model_data[, out_col_name]>0]
  
  mean(abs(pred_trn_capped - train_out_data))
  mean(abs(train_fld - pred_trn_fld))
  
  max_val = max(max(train_fld), max(pred_trn_fld))
  
  plot(pred_trn_fld, train_fld, asp=1, ylim=c(0,max_val), xlim=c(0,max_val))
  
  test_fld = test_out_data[test_out_data>0]
  pred = predict(output, newdata = as.data.frame(test_in_data), type='response')
  pred_capped = replace(pred, pred > 159, 159)
  pred_fld = pred_capped[model_data[-prt$Resample1, out_col_name]>0]
  
  max_val = max(max(test_fld), max(pred_fld))
  
  plot(pred_fld, test_fld, asp=1, ylim=c(0,max_val), xlim=c(0,max_val))
  
  all_trn = append(all_trn, train_out_data)
  all_tst = append(all_tst, test_out_data)
  all_pred_trn = append(all_pred_trn, pred_trn_capped)
  all_pred_tst = append(all_pred_tst, pred_capped)
  
}

all_trn_df = data.frame(all_trn, all_pred_trn)
trn_rmse = (mean((all_trn_df[,'all_trn'] - all_trn_df[,'all_pred_trn'])^2))^0.5
trn_mae = mean(abs(all_trn_df[,'all_trn'] - all_trn_df[,'all_pred_trn']))
all_tst_df = data.frame(all_tst, all_pred_tst)
tst_rmse = (mean((all_tst_df[,'all_tst'] - all_tst_df[,'all_pred_tst'])^2))^0.5
tst_mae = mean(abs(all_tst_df[,'all_tst'] - all_tst_df[,'all_pred_tst']))
print(trn_rmse) 
print(trn_mae)
print(tst_rmse)
print(tst_mae)

dbWriteTable(con, paste(model_type, '_count_mod_res_train', sep=""), all_trn_df, overwrite=TRUE)
dbWriteTable(con, paste(model_type, '_count_mod_res_test', sep=""), all_tst_df, overwrite=TRUE)
if (model_type == 'rf'){
  rownames(impo_df) = rownames(impo)
  colnames(impo_df) = 1:ncol(impo_df)
  dbWriteTable(con, 'rf_count_feat_impo', impo_df, overwrite=TRUE)
}

