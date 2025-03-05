import file_input as fi
import file_processing as fp
import cProfile

profile = cProfile.Profile()
profile.enable()

#计算两个集合的jaccard相似度
def jaccard_similarity(set_org,set_add):
    intersection = len(set_org & set_add)
    union = len(set_org | set_add)
    return intersection/union if union else 0.0

#计算两个文档的相似度
def document_similarity(file_processor):
    path_org = file_processor.file_paths[0]
    path_add = file_processor.file_paths[1]

    org_content = file_processor.paths_contents_pairs[path_org]
    add_content = file_processor.paths_normalized_pairs[path_add]

    #获取两个文档的2-gram
    org_set_2 = file_processor.paths_ngram_pairs_2[path_org]
    add_set_2 = file_processor.paths_ngram_pairs_2[path_add]

    #获取两个文件的3_gram
    org_set_3 = file_processor.paths_ngram_pairs_3[path_org]
    add_set_3 = file_processor.paths_ngram_pairs_3[path_add]

    #混合2-gram和3-gram计算相似度,短文本只使用2_gram快速检查
    two_gram_jaccard = jaccard_similarity(org_set_2, add_set_2)
    three_gram_jaccard = jaccard_similarity(org_set_3, add_set_3) if (len(org_content) <=1000 or len(add_content) <=1000) else 0.0
    result = (two_gram_jaccard * 0.4 + three_gram_jaccard * 0.6)

    #向答案文件中写入结果
    answer = '二者的重复度为:' +(str(result.__round__(2)))+'\n'
    fp.file_write(file_processor.file_paths[2], str(answer))

def main():
    org_file, org_add_file, answer_file = fi.read_file_from_args()
    file_processor = fp.FileProcessor([org_file, org_add_file, answer_file])

    fp.file_write(file_processor.file_paths[2], '原文件：'+file_processor.file_paths[0]+'\n')
    fp.file_write(file_processor.file_paths[2], '检查文件：'+file_processor.file_paths[1]+'\n')

    document_similarity(file_processor)
    print(fp.file_read(file_processor.file_paths[2]),end='\n\n')




if __name__ == '__main__':
    main()
    profile.disable()
    profile.dump_stats('profile.prof')