war_dict = {"China":2,"Usa":3,"Japan":1}

#sort来找出每个分类下前3的
war_dict_sorted = sorted(war_dict.items(), key=lambda x: x[1], reverse=True)

print(war_dict_sorted[0][0])

print(sum(war_dict.values()))