#include<iostream>
#include<fstream>
#include<string>
#include<cstring>
#include<vector>
#include<stdlib.h>
#include<sys/types.h>
#include<dirent.h>
#include<errno.h>
#include<limits.h>
#include<math.h>

using namespace std;

struct matchData
{
    int start;
    int end;
    int score;
};

void Tokenize(const string& str,
                      vector<int>& tokens,
                      const string& delimiters = ",")
{
    // Skip delimiters at beginning.
    string::size_type lastPos = str.find_first_not_of(delimiters, 0);
    // Find first "non-delimiter".
    string::size_type pos     = str.find_first_of(delimiters, lastPos);

    while (string::npos != pos || string::npos != lastPos)
    {
        // Found a token, add it to the vector.
        tokens.push_back(atoi((str.substr(lastPos, pos - lastPos)).c_str()));
        // Skip delimiters.  Note the "not_of"
        lastPos = str.find_first_not_of(delimiters, pos);
        // Find next "non-delimiter"
        pos = str.find_first_of(delimiters, lastPos);
    }
}


void ReadSeqDB(vector<string>& names, vector<vector<int> >& seqs, const char* fname)
{
	// Open the sequence file and read data from it
	string line;
	ifstream file(fname);
	while (! file.eof())
	{
		getline(file, line);
		if (line != "")
		{
			if (! line.find(">"))
			{
				line = line.substr(1);
				names.push_back(line);
			}
			else
			{
				vector<int> tokens;
				Tokenize(line, tokens);
				seqs.push_back(tokens);
			}
		}
	}
}


void background(vector<double>& bg, const char* fname)
{
	string line;
        ifstream file(fname);
        while (! file.eof())
        {
		getline(file, line);
		if (line != "")
		{
			bg.push_back(atof(line.c_str()));
		}
	}
}



vector<vector<int> > ProcessPWM(vector<vector<int> >& pwm, const vector<double>& bg)
{
    int row = pwm.size();
    int col = pwm[0].size();

    vector<vector<int> > pssm(row, vector<int> (col));
    for (int i = 0; i < col; i++)
    {
        int count = 0;
        for (int j = 0; j < row; j++)
            count += pwm[j][i];

        for (int j = 0; j < row; j++)
        {
            double f = (pwm[j][i] + bg[j])  / (count + 1);
            double val = 100.0 * (log(f) - log(bg[j]));
            if (val > 0.0)
                pssm[j][i] = (int) ( val + 0.5 );
            else
                pssm[j][i] = (int) ( val - 0.5 );
        }
    }
    return pssm;
}


int tresholdFromP(const vector<vector<int> >& mat, const vector<double>& bg, const double& p)
{
    int numA = mat.size();
    int n = mat[0].size();

    int maxT = 0;
    int minV = INT_MAX;

    for (int i = 0; i < n; ++i)
    {
        int max = mat[0][i];
        int min = max;
        for (int j = 1; j < numA; ++j)
        {
            int v = mat[j][i];
            if (max < v)
                max = v;
            else if (min > v)
                min = v;
        }
        maxT += max;
        if (minV > min)
            minV = min;
    }

    int R = maxT - n * minV;

    vector<double> table0(R + 1, 0.0);
    vector<double> table1(R + 1, 0.0);

    for (int j = 0; j < numA; ++j)
        table0[mat[j][0] - minV] += bg[j];

    for (int i = 1; i < n; ++i)
    {
        for (int j = 0; j < numA; ++j)
        {
            int s = mat[j][i] - minV;
            for (int r = s; r <= R; ++r)
                table1[r] += bg[j] * table0[r - s];
        }
        for (int r = 0; r <= R; ++r)
        {
            table0[r] = table1[r];
            table1[r] = 0.0;
        }
    }

    double sum = 0.0;

    for (int r = R; r >= 0; --r)
    {
        sum += table0[r];
        if (sum > p)
        {
            return (r + n * minV + 1);
        }
    }

        return n * minV;
}



vector<matchData> Search(const vector<int>& seq, const vector<vector<int> >& pwm, const int tol, const int all)
{
	int const n = seq.size();
	int const m = pwm[0].size();

	matchData hit;
	vector<matchData> res;

    int end1 = n - m;
    int end2 = m;

	for (int j = 0; j <= end1; j++)
	{
		int score = 0;
        int k;
		for (k = 0; k < end2; k++)
		{

            if (seq[j + k] == -1)
            {
                score = tol - 10;
                break;
            }
            score += pwm[seq[j + k]][k];

		}

		if (score >= tol)
		{
            hit.start = j;
            hit.end = j + k;
			hit.score = score;
			res.push_back(hit);
		}
        else
        {
            if (all == 1)
            {
                hit.start = j;
                hit.end = j + k;
                hit.score = score;
                res.push_back(hit);
            }
        }
	}
	return res;
}

