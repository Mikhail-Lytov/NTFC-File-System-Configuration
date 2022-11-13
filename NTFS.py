#Лытов Михаил ККСО-03-20

import struct
fd = open('ntfs.img','rb')
data = fd.read(400000)
sect,clust,mft,MFTmirr,size_MFT = struct.unpack('=11xHB34xQQB',data[:65])
mft_address = hex(sect * clust * mft)
MFTmirr_address = hex(sect * clust * MFTmirr)
print(' '*50, 'загрузочный сектор')
print('сектор:', sect,'\nкластер', clust)
print('адрес mft', mft_address)
print('адрес mftmirr', MFTmirr_address)
print('размер одной записи', size_MFT)
print('\n', '_' * 100, '\n')
print(' '*50, 'MFT')
name = '=' + str(mft * sect * clust) + 'x' + '4s' +'H' + 'H' + 'Q' + 'H' + 'H' + 'H' + 'H' + 'I' + 'I' + 'Q' + 'H' + '2x' + 'I'

size = mft * sect * clust + 4 + 2 + 2 + 8 + 2 + 2 + 2 + 2 + 4 + 4 + 8 + 2 + 2 + 4

signature,array_marker,number_el_marker,number_journal, serial_number,link_counter,offest_first_attribute,flag,size_used_MFT,selected_size,address_base_record,base_record_iden,file_record_number = struct.unpack(name,data[:size])
print('сигнатура', signature)
print('смещение массива маркеров:', hex(array_marker))
print('количество эллементов смещение маркеров', number_el_marker)
print('номер для журнала транзакций', hex(number_journal))
print('порядковый номер', serial_number)
print('счетчик ссылок', link_counter)
print('смещение первого атрибута', hex(offest_first_attribute))
print('запись используется', hex(flag))
print('используемы размер записи MFT', size_used_MFT)
print('выделенный размер записи MFT', selected_size)
print('адрес базовой записи MFT', address_base_record)
print('индетификатор для нового атрибута', base_record_iden)
print('номер файловой записи ', file_record_number)

print('\n','_'*100, '\n')
print(' '*50, 'атрибуты')
arr = mft * sect * clust  
size_1 = arr
name_1 = '=' + str(size_1) + 'x'
#for namber in range(number_el_marker):

chek= 0
while chek != 4294967295:
	attribute_type_identifier, length_attributes, flag_residency, line_name_attribute, name_offset, flag_att, attribute_ID = struct.unpack(f"{size_1 + offest_first_attribute}xIIBBHHH", data[:size_1+offest_first_attribute + 16])
	print('индетификатор типа атрибута', hex(attribute_type_identifier))
	print('длина атрибуты', hex(length_attributes), '=', length_attributes)
	if line_name_attribute == 0:
		print('атрибут безымянный')
	else:
		print('длина имени', line_name_attribute)
		print('смещение имени', hex(name_offset), '=', name_offset)
	print('флаги', flag_att)
	print('индетификатор атрибута', attribute_ID)
	if flag_residency !=1:
		print("Атрибут резидентный")
		line_content_att, content_offset = struct.unpack(f"{size_1+offest_first_attribute+16}xIH", data[:size_1+offest_first_attribute+22])
	else:
		print("Атрибут нерезидентный")
		line_content_att, content_offset == None
		
		virtual_cluster, final_virtual_cluster, series_list_offset, compression_unit, unused, selected_size, actual_size, initiated_size, compression_size = struct.unpack(f"={size_1+offest_first_attribute+16}xQQHHIQQQQ", data[:size_1+offest_first_attribute+72])
		print("Доп. параметры нерезидентного атрибута:")
		print("Начальный виртуальный кластер:",virtual_cluster) 
		print("Конечный виртуальный кластер:", final_virtual_cluster)
		print("Смещение списка серий:", series_list_offset)
		print("Размер блока сжатия:", compression_unit)
		print("Не используется:", unused)
		print("Выделенный размер содержимого атрибута:", hex(selected_size), '=', selected_size)
		print("Фактический размер атрибута:", hex(actual_size), '=', actual_size) 
		print("Инициализированный размер атрибута:", hex(initiated_size), '=', initiated_size)
		print("Размер атрибута после сжатия:", compression_size)

	print("Длина содержимого:", line_content_att)
	print("Смещение содержимого:", content_offset)

	#name_2 = '=' + str(size_1 + content_offset) + 'x' +  str(line_content_att) + 's' +'B'
	#size_2 = size_1 + content_offset + line_content_att +1
	#text, a = struct.unpack(name_2,data[:size_2]) 
	#print('тект:', str(text))

	corr, chek = struct.unpack(f"={size_1+offest_first_attribute+length_attributes-1}xBI", data[:size_1+offest_first_attribute+length_attributes+4])
	size_1 = size_1+length_attributes
	print("_" * 100)
	#print(hex(size_1))
print("конец записи")


