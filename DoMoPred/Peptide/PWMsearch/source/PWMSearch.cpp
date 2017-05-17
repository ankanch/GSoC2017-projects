#include "search.cpp"
#include <iostream>
#include <vector>
#include <string>
#include <Python.h>
#include <sstream>

using namespace std;

vector<vector<int> > seqdb;
vector<string> names;
vector<vector<int> > pssm;
vector<double> bg;

static PyObject *SequenceDB(PyObject * self, PyObject * args)
{
	const char *file;

	if (!PyArg_ParseTuple(args, "s", &file))
	{
		return NULL;
	}

	//cout << "Processing sequence database file: "<< file << endl;
	ReadSeqDB(names, seqdb, file);
	Py_DECREF(file);
	return Py_BuildValue("");
}


static PyObject *Sequence(PyObject * self, PyObject * args)
{
	PyObject *input;
	Py_ssize_t sz;

	if (!PyArg_ParseTuple(args, "O", &input))
	{
		return NULL;
	}

	//cout << "Processing sequence" << endl;

	sz = PyList_Size(input);
	seqdb.clear();
	names.clear();

	vector<int> lst;
	for (int i = 0; i < sz; i++)
	{
		lst.push_back(PyInt_AsLong(PyList_GetItem(input, i)));
	}

	seqdb.push_back(lst);
	names.push_back("input_seq");

	//Py_DECREF(input);
	return Py_BuildValue("");
}


static PyObject *LoadPWM(PyObject * self, PyObject * args)
{
	PyObject *input;
	Py_ssize_t sz;

	if (!PyArg_ParseTuple(args, "O", &input))
	{
		return NULL;
	}

	//cout << "Processing PWM file" << endl;

	sz = PyList_Size(input);
	pssm.clear();

	vector<vector<int> > pwmdt;

	for (int i = 0; i < sz; i++)
	{
		PyObject *list = PyList_GetItem(input, i);
		Py_ssize_t seq_sz = PyList_Size(list);
		vector<int> lst;
		for (int j = 0; j < seq_sz; j++)
		{
			lst.push_back(PyInt_AsLong(PyList_GetItem(list, j)));
		}
		pwmdt.push_back(lst);
	}

	pssm = ProcessPWM(pwmdt, bg);

	Py_DECREF(input);
	return Py_BuildValue("");
}


static PyObject *Threshold(PyObject * self, PyObject * args)
{

	double pval;

    if (!PyArg_ParseTuple(args, "d", &pval))
    {
        return NULL;
    }

	int tol = tresholdFromP(pssm, bg, pval);

	return Py_BuildValue("i", tol);
}


static PyObject *BackGround(PyObject * self, PyObject * args)
{
	const char *file;

	if (!PyArg_ParseTuple(args, "s", &file))
	{
		return NULL;
	}

	//cout << "Processing background file: "<< file << endl;
	background(bg, file);
	//Py_DECREF(file);
	return Py_BuildValue("");
}



static PyObject *ScanDB(PyObject * self, PyObject * args)
{
	//PyObject *list;
	//vector<vector<int> > pssm;
	int tol;
	int all = 0;

    if (!PyArg_ParseTuple(args, "i|i", &tol, &all))
    {
        return NULL;
    }

	//cout << "Scanning the database with pval: " << pval << endl;

	//list = (PyObject *) PyList_New(0);
	PyObject *dict = PyDict_New();
	//pssm = ProcessPWM(pwmdt, bg);
	//int tol = tresholdFromP(pssm, bg, pval);
    //    cout << tol;
	int sz = seqdb.size();
	vector<matchData> res;
	for (int s = 0; s < sz; s++)
		{
			res = Search(seqdb[s], pssm, tol, all);
			int rsz = res.size();
			if (rsz > 0)
			{
				//string ret = names[s];
				PyObject *dict_tmp = PyDict_New();
				for (int r = 0; r < rsz; r++)
					{
						//stringstream stt, end, scr;
						//stt << res[r].start;
						//end << res[r].end;
						//scr << res[r].score; // change made to add score
						//ret += "|" + out.str() + ":" + scr.str(); // change made to add score

						PyDict_SetItem(dict_tmp, Py_BuildValue("(i, i)", res[r].start, res[r].end), Py_BuildValue("i", res[r].score));
					}
				//PyList_Append(list, Py_BuildValue("s", ret.c_str()));
				PyDict_SetItem(dict, Py_BuildValue("s", names[s].c_str()), dict_tmp);
			}
		}

	//return list;
	return dict;
}


static PyMethodDef PWMSearch_methods[] =
{
	{"SequenceDB", SequenceDB, METH_VARARGS, "Load sequence data base fasta file"},
	{"Sequence", Sequence, METH_VARARGS, "Load sequence"},
	{"LoadPWM", LoadPWM, METH_VARARGS, "Read PWM"},
	{"Threshold", Threshold, METH_VARARGS, "Calculate threshold for a given PWM and bg"},
	{"BackGround", BackGround, METH_VARARGS, "Load background data"},
	{"ScanDB", ScanDB, METH_VARARGS, "Scan Database"},
	{NULL, NULL}
};

PyMODINIT_FUNC initPWMSearch()
{
    Py_InitModule("PWMSearch", PWMSearch_methods);

    //import_array();
}
