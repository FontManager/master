//
// The Fontaine Font Analysis Project 
// 
// Copyright (c) 2009 by Edward H. Trager
// All Rights Reserved
// 
// Released under the GNU GPL version 2.0 or later.
//     


//
// Kokuji.h
//

#ifndef ORTHOGRAPHY_DATA
#include "../OrthographyData.h"
#endif

#ifndef KOKUJI
#define KOKUJI

namespace Kokuji{

//
// 国字 (和制汉字)
// Updated 2015.07.01 by ET
// Sources:
//
// (1) http://kanjitisiki.com/kokuzi/
// (2) http://blog.lingualift.com/kanji-made-in-japan/
// (3) http://www.sljfaq.org/afaq/kokuji-list.html
//
UINT32 values[]={
	0x4FE3, // 俣
	0x4FE4, // 俤
	0x4FE5, // 俥
	0x50CD, // 働
	0x51E7, // 凧
	0x51E9, // 凩
	0x51EA, // 凪
	0x5301, // 匁
	0x5302, // 匂
	0x53FA, // 叺
	0x544E, // 呎
	0x54D8, // 哘
	0x55B0, // 喰
	0x5678, // 噸
	0x567A, // 噺
	0x5726, // 圦
	0x5737, // 圷
	0x5738, // 圸
	0x5788, // 垈
	0x5840, // 塀
	0x5870, // 塰
	0x5B36, // 嬶
	0x5C76, // 屶
	0x5CBC, // 岼
	0x5CC5, // 峅
	0x5CE0, // 峠
	0x5F16, // 弖
	0x603A, // 怺
	0x6268, // 扨
	0x643E, // 搾
	0x6741, // 杁
	0x6762, // 杢
	0x6763, // 杣
	0x6764, // 杤
	0x67A0, // 枠
	0x67A1, // 枡
	0x67FE, // 柾
	0x6802, // 栂
	0x6803, // 栃
	0x685D, // 桝
	0x68BA, // 梺
	0x6919, // 椙
	0x691A, // 椚
	0x691B, // 椛
	0x6921, // 椡
	0x6923, // 椣
	0x6925, // 椥
	0x6928, // 椨
	0x697E, // 楾
	0x6981, // 榁
	0x698A, // 榊
	0x69DD, // 槝
	0x6A2B, // 樫
	0x6A2E, // 樮
	0x6A61, // 橡
	0x6A72, // 橲
	0x6B1F, // 欟
	0x6BDF, // 毟
	0x6C62, // 汢
	0x7195, // 熕
	0x71F5, // 燵
	0x74E7, // 瓧
	0x74E9, // 瓩
	0x74F0, // 瓰
	0x74F1, // 瓱
	0x74F2, // 瓲
	0x74F8, // 瓸
	0x7505, // 甅
	0x7551, // 畑
	0x7560, // 畠
	0x7569, // 畩
	0x766A, // 癪
	0x7872, // 硲
	0x7874, // 硴
	0x7ACD, // 竍
	0x7ACF, // 竏
	0x7AD3, // 竓
	0x7AD5, // 竕
	0x7AE1, // 竡
	0x7AF0, // 竰
	0x7B02, // 笂
	0x7B39, // 笹
	0x7C13, // 簓
	0x7C17, // 簗
	0x7C4F, // 籏
	0x7C75, // 籵
	0x7C7E, // 籾
	0x7C81, // 粁
	0x7C82, // 粂
	0x7C8D, // 粍
	0x7CA8, // 粨
	0x7CAD, // 粭
	0x7CC0, // 糀
	0x7CCE, // 糎
	0x7CD8, // 糘
	0x7D9B, // 綛
	0x7E05, // 縅
	0x7E67, // 繧
	0x7E83, // 纃
	0x7E90, // 纐
	0x8062, // 聢
	0x817A, // 腺
	0x81A4, // 膤
	0x81B5, // 膵
	0x825D, // 艝
	0x8422, // 萢
	0x84D9, // 蓙
	0x8630, // 蘰
	0x86AB, // 蚫
	0x86EF, // 蛯
	0x87D0, // 蟐
	0x88B0, // 袰
	0x88C3, // 裃
	0x88C4, // 裄
	0x8904, // 褄
	0x8977, // 襷
	0x8ADA, // 諚
	0x8EBE, // 躾
	0x8EC8, // 軈
	0x8F4C, // 轌
	0x8FB7, // 辷
	0x8FBB, // 辻
	0x8FBC, // 込
	0x8FDA, // 迚
	0x9027, // 逧
	0x9056, // 遖
	0x92F2, // 鋲
	0x9335, // 錵
	0x933A, // 錺
	0x933B, // 錻
	0x93B9, // 鎹
	0x9453, // 鑓
	0x958A, // 閊
	0x9596, // 閖
	0x96EB, // 雫
	0x9786, // 鞆
	0x9790, // 鞐
	0x98AA, // 颪
	0x9942, // 饂
	0x9B96, // 鮖
	0x9B97, // 鮗
	0x9BA0, // 鮠
	0x9BB4, // 鮴
	0x9BCF, // 鯏
	0x9BD1, // 鯑
	0x9BD2, // 鯒
	0x9BF0, // 鯰
	0x9BF1, // 鯱
	0x9BF2, // 鯲
	0x9C2F, // 鰯
	0x9C30, // 鰰
	0x9C47, // 鱇
	0x9C48, // 鱈
	0x9C5A, // 鱚
	0x9CF0, // 鳰
	0x9D2B, // 鴫
	0x9D46, // 鵆
	0x9D64, // 鵤
	0x9DAB, // 鶫
	0x9EBF, // 麿
	END_OF_DATA
};

//
// Sample sentences
// 
const char *sentences[]={
	"碓氷峠（うすいとうげ）は群馬県安中市松井田町と長野県北佐久郡軽井沢町との境にある日本の峠である。",
	END_OF_DATA
};


//
// 
//
OrthographyData data={
	"Japanese Kokuji",
	"日本国字 (和制汉字)",
	0x5ce0, // Mountain pass, 峠 
	values,
	"峠栂込榊鴫辻畑柾梻毟",
	sentences
};

const OrthographyData *pData = &data;

}; // end of namespace

#endif
