#include <stdio.h>
#include "DxLib.h"
#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <Windows.h>




///
/// 機能アイデアまとめ
/// ①：なでなで機能
///		→なでなでの回数によって言葉が変化。
///		　デレデレした言葉をロシア語で喋ってくれる機能
/// ②：標準で時間を表示する機能
///		→どうやって普通のセリフに切り替える？
/// 
/// GITにあげよう、ギトギトを
/// git add .




/*
LRESULT CALLBACK WndProc(HWND hwnd, UINT message, WPARAM wParam, LPARAM lParam) 
{
	switch (message) {
	case WM_DESTROY:
		PostQuitMessage(0);
		return 0;
	case WM_LBUTTONDOWN:
		//マウス左ボタン押下
		return 0;
	}
	return DefWindowProc(hwnd, message, wParam, lParam);
}*/


int Enter_chk(const char *centence)
{
	int counter = 0;
	const char* match = "\n";
	const char* centence_ptr = centence;
	while (true){
		centence_ptr = strstr(centence_ptr, match);
		if (centence_ptr != NULL)
		{
			counter++;
			centence_ptr++;
		}
		else
			break;
	}
	return counter + 1;
}

void preInitialize(int *width,int *height)
{
	RECT rc;
	GetWindowRect(GetDesktopWindow(), &rc);
	*width = rc.right - rc.left;
	*height = rc.bottom - rc.top;
	SetGraphMode(*width, *height, 32); 
	ChangeWindowMode(TRUE); 
	SetWindowStyleMode(2); 
	SetUseBackBufferTransColorFlag(TRUE); 
}

void afterInitialize() {
	HWND hWnd = GetMainWindowHandle();
	SetWindowPos(hWnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE);
	SetAlwaysRunFlag(TRUE);
	SetDrawScreen(DX_SCREEN_BACK);
}

void mainsystem(int width, int height)
{
	int Cr = GetColor(255, 204, 255);
	int Arisa_Meido = LoadGraph(u8"アーリャメイド服.png");
	int Arisa_Seifuku = LoadGraph(u8"アーリャ制服.png");
	int Maria_Tenshi = LoadGraph(u8"マーシャ天使.png");
	int fukidashi = LoadGraph(u8"吹き出し画像.png");
	SetFontSize(35);
	int FontHandle = CreateFontToHandle(NULL, 40, 3);
	int SELECT_GRAPH = Arisa_Meido;
	int SELECT_WORD = 6;
	time_t now = time(NULL);
	struct tm* pnow = localtime(&now);
	POINT po;

	static char Serifu[][100] = {
			u8"Не уходи...♥",
			u8"テッテッテ、\nテーストー",
			u8"カッコいい系\n女子、正直スコです。",
			u8"なでなで検知\nいい感じ",
			u8"三行用の\nテスト\nしちゃう？！",
			u8"Адкий\nлюбитель\nженских\nножек",
			u8"うおおおおおおお\nこれでどうじゃあああ!!",
	};

	while (ProcessMessage() == 0)
	{
		ClearDrawScreen();
		DrawGraph(width - 250, height - 450, SELECT_GRAPH,TRUE);//キャラ描画
		DrawGraph(width - 400, height - 650, fukidashi, TRUE);//吹き出し描写
		///\nの数によって行数を判別//
		if (Enter_chk(Serifu[SELECT_WORD]) == 1) 
		{
			SetFontSize(35);
			DrawString(width - 365, height - 540, Serifu[SELECT_WORD], Cr);//台詞描写１行
		}
			
		else if (Enter_chk(Serifu[SELECT_WORD]) == 2) 
		{
			SetFontSize(35);
			DrawString(width - 365, height - 560, Serifu[SELECT_WORD], Cr);//台詞描写２行
		}
			
		else if (Enter_chk(Serifu[SELECT_WORD]) == 3)
		{
			SetFontSize(30);
			DrawString(width - 365, height - 570, Serifu[SELECT_WORD], Cr);//台詞描写3行
		}
		else if (Enter_chk(Serifu[SELECT_WORD]) == 4)
		{
			SetFontSize(25);
			DrawString(width - 365, height - 580, Serifu[SELECT_WORD], Cr);//台詞描写4行
		}
			
		ScreenFlip();

		if (CheckHitKey(KEY_INPUT_1)) {
			SELECT_GRAPH = Arisa_Meido;
		}
		if (CheckHitKey(KEY_INPUT_2)) {
			SELECT_GRAPH = Arisa_Seifuku;
		}
		if (CheckHitKey(KEY_INPUT_3)) {
			SELECT_GRAPH = Maria_Tenshi;
		}


		///////なでなで機能問題点
		///////撫でてる最中のアニメーションが欲しい
		if (GetKeyState(VK_LBUTTON) & 0x80) {//左クリ
			GetCursorPos(&po);
			if (po.x >= width - 250 and po.y >= height - 450)
			{
				//SELECT_GRAPH = Arisa_Seifuku;
				DWORD start_time = ::GetTickCount64();
				DWORD now_time = NULL;
				int move_distance = 0;
				int defalt_point = po.x;
				while (now_time < 500)//マウスの移動距離計算
				{
					now_time = ::GetTickCount64() - start_time;
					Sleep(5);
					move_distance += abs(po.x-defalt_point);
					GetCursorPos(&po);
				}
				if (GetKeyState(VK_LBUTTON) & 0x80 and move_distance >= 500*2*5 and abs(po.x-defalt_point) < 500)//基準値*なでなで（往復）回数をチェック、同時にポインターが離れ過ぎてないか確認
				{
					SELECT_WORD = 3;
				}
			}
		}
		/*if (GetKeyState(VK_RBUTTON) & 0x80) {//右クリ
			GetCursorPos(&po);
			if (po.x >= width - 250 and po.y >= height - 450)
				SELECT_GRAPH = Arisa_Seifuku;
		}*/
		if (CheckHitKey(KEY_INPUT_Q)) {
			DeleteGraph(Arisa_Meido);
			break;
		}
	}
}


int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
	int width = NULL;
	int height = NULL;
	SetUseCharCodeFormat(DX_CHARCODEFORMAT_UTF8);
	preInitialize(&width, &height);
	if (DxLib_Init() == -1)
		return -1;
	afterInitialize();
	mainsystem(width, height);
	DxLib_End();
	return 0;
}