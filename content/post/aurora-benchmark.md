+++
date = "2016-09-07T11:57:11-04:00"
title = "Benchmarking Amazon's Aurora"
draft = false
toc = true
tags = ["aws"]
categories = ["Cloud Engineering", "Database"]
series = []
comment = true

+++


I saw this study by the folks over at [Google and their 2nd Generation Cloud SQL](https://cloudplatform.googleblog.com/2016/08/Cloud-SQL-Second-Generation-performance-and-feature-deep-dive.html).

The results they posted didn't exactly mirror what I saw when running the benchmarks for myself.
You can get the raw data here @ [Github.](https://github.com/2ndWatch/aurora_benchmark)

Everything was stood up using Terraform, the benchmark tests were conducted using Sysbench, and all data was plotted using R.


Since we didn't have access to Google's original data, we provided some overlays in the post as an easy visual comparison. However the data used to produce all of those graphs as well as additional data is in the repo.

[Read More @ 2ndwatch.com](http://2ndwatch.com/blog/benchmarking-amazon-aurora/)
