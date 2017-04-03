
# mirror url for reference: "http://cran.us.r-project.org"
library(rpart)
library(rpart.plot)
library(RSQLite)
library(DBI)
base_dir<- "C:/Users/Jeff/Documents/research/Sadler_3rdPaper/manuscript/"
data_dir<- paste(base_dir, "Data/", sep="")
fig_dir <- paste(base_dir, "Figures/general/", sep="")
db_filename <- "floodData.sqlite"
print(paste(data_dir, db_filename))
con = dbConnect(RSQLite::SQLite(), dbname=paste(data_dir, db_filename, sep=""))

dbListTables(con)

df = dbReadTable(con, 'for_model')
df = subset(df, rain_daily_sum>0.1)
df = df[!is.na(df$gw_daily_avg),]

short_names = c('rd', 'rhr', 'r15', 'r3d', 'gw', 'td', 'wd')
in_cols = c(1:6, 8)
colnames(df)[in_cols] = short_names
in_col_names = colnames(df)[in_cols]
out_col_name = 'flooded'
data = df[, c(in_col_names, out_col_name)]

fmla = as.formula(paste(out_col_name, "~", paste(in_col_names, collapse="+")))
fmla

fit = rpart(fmla, method='class', data=data, minsplit=1)

printcp(fit)

plot(fit)
text(fit, use.n=TRUE, all=TRUE, cex=.8)

prp(fit, type=4)
tiff(paste(fig_dir, "Plot2.tif"), width=9, height=6, units='in', res = 300)
rpart.plot(fit, under=TRUE, cex=0.9, extra=1, varlen = 6)
dev.off()


