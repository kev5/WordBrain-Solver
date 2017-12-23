// Copyright 2017 Keval Khara kevalk@bu.edu

#include <iostream>
#include <string.h>
#include <fstream>
#include <stdio.h>
#define maxnod 1200005
void firstCall(char mat[15][15],int step);
void circleCall(int x,int y,char mat[15][15],int step,int now,std::string temp,int cur);

int son[maxnod][26];
int haslength[maxnod][20];
int is_word[maxnod];
int length[105];
int tot=1;
int n,m,k;
int task=0;
std::string s[105];
std::string ch[15];
std::string ans[15];
char road[105][26][26];


void ins(std::string s)
{
	int len=s.size();
	int now=1;
	for (int i=0;i<s.size();i++)
	{
		haslength[now][len]=1;
		if (!son[now][s[i]-'a']) son[now][s[i]-'a']=++tot;
		now=son[now][s[i]-'a'];
	}
	haslength[now][len]=1;
	is_word[now]=1;
	return;
}
void init1()
{
	std::ifstream fin1("large_word_list.txt");
	std::string s;
	while (fin1>>s)
		ins(s);
}

void circleCall(int x,int y,char mat[15][15],int step,int now,std::string temp,int cur)
{
//	if (task==2) cout<<temp<<endl;
	if (!haslength[cur][length[step]]) return;
	char pre=mat[x][y];
	mat[x][y]=0;
	if (now==s[step].size())
	{
		char nex[15][15];
		memset(nex,0,sizeof(nex));
		for (int j=1;j<=m;j++)
		{
			int tt=n;
			for (int i=n;i>=1;i--)
			if (mat[i][j]!=0)
			{
				nex[tt][j]=mat[i][j];
				tt--;
			}
		}
		ans[step]=temp;
		for (int i=1;i<=n;i++)
			for (int j=1;j<=m;j++)
				road[step][i][j]=nex[i][j];
		if (is_word[cur]==1)
		{
			firstCall(nex,step+1);
		}
		mat[x][y]=pre;
		return;
	}
	for (int fx=-1;fx<=1;fx++)
	for (int fy=-1;fy<=1;fy++)
	if (fx!=0 || fy!=0)
	{
		int nex,ney;
		nex=x+fx; ney=y+fy;
		if (nex<1 || nex>n || ney<1 || ney>m) continue;
		if (mat[nex][ney]==0) continue;
		if (s[step][now]!='*' && s[step][now]!=mat[nex][ney]) continue;
		if (son[cur][mat[nex][ney]-'a']==0) continue;
		circleCall(nex,ney,mat,step,now+1,temp+mat[nex][ney],son[cur][mat[nex][ney]-'a']);
	}
	mat[x][y]=pre;
	return;
}

void out(char mat[15][15])
{
	for (int i=1;i<=n;i++)
	{
		for (int j=1;j<=m;j++)
		if (mat[i][j]==0)
			std::cout<<"*";
		else
			std::cout<<mat[i][j];
		std::cout<<std::endl;
	}
}

void firstCall(char mat[15][15],int step)
{
	if (step==k+1)
	{
		for (int i=1;i<=k;i++)
			std::cout<<ans[i]<<' ';
		std::cout<<std::endl;
//		for (int now=1;now<=k;now++)
//		{
//			for (int i=1;i<=n;i++)
//			{
//				for (int j=1;j<=m;j++)
//				if (road[now][i][j]==0)
//					cout<<"*";
//				else
//					cout<<road[now][i][j];
//				cout<<endl;
//			}
//			cout<<endl;
//		}
//		cout<<"***********************"<<endl;
		return;
	}
	std::string aa="";
	for (int i=1;i<=n;i++)
		for (int j=1;j<=m;j++)
		if (mat[i][j]!=0 && son[1][mat[i][j]-'a']!=0 && (s[step][0]=='*' || s[step][0]==mat[i][j]))
			circleCall(i,j,mat,step,1,aa+mat[i][j],son[1][mat[i][j]-'a']);
}

void init2()
{
	std::ifstream fin2("puzzles.txt");
	while (fin2>>n>>m>>k)
	{
		task++;
		for (int i=1;i<=n;i++)
			fin2>>ch[i];
		for (int i=1;i<=k;i++)
		{
			fin2>>s[i];
			length[i]=s[i].size();
		}
		char mat[15][15];
		for (int i=1;i<=n;i++)
			for (int j=1;j<=m;j++)
				mat[i][j]=ch[i][j-1];
		firstCall(mat,1);
		std::cout<<"task"<<task<<" finish"<<std::endl;
//		while (1);
	}
}
int main()
{
//	freopen("ans.txt","w",stdout);
	init1();
	init2();
}
