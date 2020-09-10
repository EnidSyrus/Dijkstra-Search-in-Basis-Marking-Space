# Dijkstra Search in Basis Marking Space

This repository is the codes of our program that realizes Algorithm 1 in the paper "Determining Optimal Control Sequences for Reconfiguration in Petri Nets" (called the paper in the sequel). Moreover, three benchmarks are reported in <B>Benchmark_Recon.pdf</B>.

The program is written in Python 3. Its <B> entry point</B> is file <B>Basis.py</B>.

# Inputs and Outputs of Basis.py

## Input of the program includes:
  * The <B>Pre</B> and <B>Post</B> matrices of a plant net. They are stored in files <B>Pre.txt</B> and <B>Post.txt</B>, respectively.
  * A source marking <B>Ms</B>, a target marking set (<B>w, k</B>), a forbidden marking set (<B>z, b</B>), and a nonnegative cost vector <B>c</B>. They are stored in file <B>inputs.txt</B> line by line;
  * A set of pre-defined explicit transitions which is stored in file <B>TE.txt</B>;
  * Therefore, the total input for <B>Basis.py</B> can be viewed as [<B>Pre, Post, Ms, w, k, z, b, c, TE</B>]. Please see below for more details.

## Output of the program (output.txt):
The program performs a search (Algorithm 1 in the paper) and outputs the following results:
 * The <u>actually used</u> explicit transition set <B>TE-act</B> (which may *NOT* be the set <B>TE</B> inputted from <B>TE.txt</B>, see the note (2) below).
 * <B>Running time</B> of the program.
 * <B>graph size</B>: the size of the searched space.
 * <B>sigma_min</B>: the length of an optimal control sequence that drives the plant from marking <B>Ms</B> to set <B>Mtarget</B>.
 * <B>cmin</B>: the minimum cost of control sequence <B>sigma_min</B>.
 * The transitions sequence of <B>sigma_min</B> is given in the form <B>y1-t1-y2-t2-… </B>where each <B>yi</B> is a firing vector of the implicit subnet.
 * All data above are saved in file <B>output.txt</B>. (If the file already exists, it will be overwritten).

# Notes:
1. The input files <B>Pre.txt</B>, <B>Post.txt</B>, <B>inputs.txt</B>, <B>TE.txt</B> are read in by module <B>readin.py</B>. Normally they should be in the same folder of <B>readin.py</B>. For readers convenience, here we also provide the input files of the examples in <B>Benchmark_Recon.pdf</B> in several separated folders. You need to copy them to the same folder of the program when using them.
  
2. The program will check if the set <B>TE</B> read in from <B>TE.txt</B> satisfies two rules of transition selection in the paper. If not, it will automatically *add* some transitions to <B>TE</B> according to those rules. In such a case, the program will use a new set <B>TE-act</B> that is a superset of the set <B>TE</B> defined in <B>TE.txt</B>.

3. We also provide a program of the ILP-based search algorithm in the paper. It is in folder <B>ILP_Basis_Dijkstra</B> with entry point <B>Basis_ILP.py</B> that has the same format of inputs. It requires Gurobi 9.0 as the ILP solver.