import file_input as fi
import file_processing as fp

#计算两个集合的jaccard相似度
def jaccard_similarity(set_org,set_add):
    intersection = len(set_org & set_add)
    union = len(set_org | set_add)
    return intersection/union if union else 0.0

#计算两个文档的相似度
def document_similarity(file_processor):
    path_org = file_processor.file_paths[0]
    path_add = file_processor.file_paths[1]
    org_set = file_processor.paths_ngram_pairs[path_org]
    add_set = file_processor.paths_ngram_pairs[path_add]

    #向答案文件中写入结果
    answer = '二者的重复度为:' +(str( jaccard_similarity(org_set,add_set).__round__(2)))+'\n'
    fp.file_write(file_processor.file_paths[2], str(answer))

