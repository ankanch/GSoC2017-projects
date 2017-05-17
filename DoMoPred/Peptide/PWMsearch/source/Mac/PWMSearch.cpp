#include "search.cpp"
#include <iostream>
#include <vector>
#include <string>
#include <Python.h>
#include <sstream>

using namespace std;

vector<vector<int> > seqdb;
vector<string> names;
vector<vector<int> > pwmdt;
vector<double> bg;

static PyObject *SequenceDB(PyObject * self, PyObject * args)
{
	const char *file;

	if (!PyArg_ParseTuple(args, "s", &file))
	{
		return NULL;
	}

	cout << "Processing sequence database file: "<< file << endl;
	ReadSeqDB(names, seqdb, file);
	Py_DECREF(file);
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
	
	cout << "Processing PWM file" << endl;	

	sz = PyList_Size(input);
	pwmdt.clear();
	
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
	Py_DECREF(input);
	return Py_BuildValue("");
}


static PyObject *BackGround(PyObject * self, PyObject * args)
{
	const char *file;

	if (!PyArg_ParseTuple(args, "s", &file))
	{
		return NULL;
	}

	cout << "Processing background file: "<< file << endl;
	background(bg, file);
	Py_DECREF(file);
	return Py_BuildValue("");
}



static PyObject *ScanDB(PyObject * self, PyObject * args)
{
	PyObject *list;	
	vector<vector<int> > pssm;
	double pval;	
	
        if (!PyArg_ParseTuple(args, "d", &pval))
        {
                return NULL;
        }

	cout << "Scanning the database with pval: " << pval << endl;
	
	list = (PyObject *) PyList_New(0);
	pssm = ProcessPWM(pwmdt, bg);
	int tol = tresholdFromP(pssm, bg, pval);
        cout << tol;
	int sz = seqdb.size();
	vector<matchData> res;
	for (int s = 0; s < sz; s++)
		{
			res = Search(seqdb[s], pssm, tol);
			int rsz = res.size();
			if (rsz > 0)
			{
				string ret = names[s];
				for (int r = 0; r < rsz; r++)
					{
						stringstream out, scr;
						out << res[r].position;
						scr << res[r].score; // change made to add score
						ret += "|" + out.str() + ":" + scr.str(); // change made to add score
					}
				PyList_Append(list, Py_BuildValue("s", ret.c_str()));
			}
		}
 
	return list;
}


static PyMethodDef PWMSearch_methods[] = 
{
	{"SequenceDB", SequenceDB, METH_VARARGS, "Load sequence data base"},
	{"LoadPWM", LoadPWM, METH_VARARGS, "Read PWM"},
	{"BackGround", BackGround, METH_VARARGS, "Load background data"},
	{"ScanDB", ScanDB, METH_VARARGS, "Scan Database"},
	{NULL, NULL}
};

PyMODINIT_FUNC initPWMSearch()
{
    Py_InitModule("PWMSearch", PWMSearch_methods);

    //import_array();
}
