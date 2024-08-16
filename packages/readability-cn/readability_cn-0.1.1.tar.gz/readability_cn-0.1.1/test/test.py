import readability_cn

readability = ChineseReadability()
# add new custom words
readability.add_custom_words(['日志易', '优特捷'])

# Compare readability metrics before and after file changes
# 对比文件变更前后的可读性指标
readability.analyze('old.adoc', 'new.adoc')
