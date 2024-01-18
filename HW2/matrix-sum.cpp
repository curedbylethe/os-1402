#include <iostream>
#include <fstream>
#include <vector>
#include <omp.>
#include <memory>


class Matrix {
private:
    std::vector<std::vector<int>> matrix;
    int rows;
    int cols;

public:
    Matrix(int rows, int cols) : rows(rows), cols(cols) {
        matrix = std::vector<std::vector<int>>(rows, std::vector<int>(cols, 0));
    }

    Matrix(const std::vector<std::vector<int>>& matrix) : matrix(matrix) {
        rows = matrix.size();
        cols = matrix[0].size();
    }

    int getRows() const {
        return rows;
    }

    int getCols() const {
        return cols;
    }

    int get(int i, int j) const {
        return matrix[i][j];
    }

    void set(int i, int j, int value) {
        matrix[i][j] = value;
    }

    void setRow(int i, std::vector<int> row) {
        matrix[i] = row;
    }

    Matrix operator+(const Matrix& other) const {
        if (rows != other.rows || cols != other.cols) {
            std::cerr << "Error: Cannot add matrices of different dimensions" << std::endl;
            exit(EXIT_FAILURE);
        }

        Matrix result(rows, cols);

        #pragma omp parallel for num_threads(4)
        for (int i = 0; i < rows; ++i) {
            #pragma omp parallel for num_threads(4)
            for (int j = 0; j < cols; ++j) {
                result.set(i, j, matrix[i][j] + other.matrix[i][j]);
            }
        }

        return result;
    }

    Matrix operator*(const Matrix& other) const {
        if (cols != other.rows) {
            std::cerr << "Error: Cannot multiply matrices of incompatible dimensions" << std::endl;
            exit(EXIT_FAILURE);
        }

        Matrix result(rows, other.cols);

        #pragma omp parallel for num_threads(4)
        for (int i = 0; i < rows; ++i) {
            #pragma omp parallel for num_threads(4)
            for (int j = 0; j < other.cols; ++j) {
                int sum = 0;
                #pragma omp parallel for num_threads(4)
                for (int k = 0; k < cols; ++k) {
                    sum += matrix[i][k] * other.matrix[k][j];
                }
                result.set(i, j, sum);
            }
        }

        return result;
    }

    Matrix operator*(int scalar) const {
        Matrix result(rows, cols);

        #pragma omp parallel for num_threads(4)
        for (int i = 0; i < rows; ++i) {
            #pragma omp parallel for num_threads(4)
            for (int j = 0; j < cols; ++j) {
                result.set(i, j, matrix[i][j] * scalar);
            }
        }

        return result;
    }
};

Matrix readMatrixFromFile(const std::string& fileName) {
    std::ifstream file(fileName);
    if (!file.is_open()) {
        std::cerr << "Error: Unable to open file " << fileName << std::endl;
        exit(EXIT_FAILURE);
    }

    int rows, cols;
    file >> rows >> cols;

    Matrix matrix(rows, cols);

    for (int i = 0; i < rows; ++i) {
        std::vector<int> row(cols);
        for (int j = 0; j < cols; ++j) {
            file >> row[j];
        }
        matrix.setRow(i, row);
    }

    return matrix;
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <matrix_file> <num_threads>" << std::endl;
        return EXIT_FAILURE;
    }

    std::string fileName = argv[1];
    int numThreads = std::stoi(argv[2]);

    // Read matrix from file
    Matrix matrix = readMatrixFromFile(fileName);

    // Get matrix dimensions
    int rows = matrix.getRows();
    int cols = matrix.getCols();

    // Variables to store the sum
    int sum = 0;

    // Use OpenMP to parallelize the loop and calculate the sum
    #pragma omp parallel for num_threads(numThreads) reduction(+:sum)
    for (int i = 0; i < rows; ++i) {
        #pragma omp parallel for num_threads(numThreads) reduction(+:sum)
        for (int j = 0; j < cols; ++j) {
            sum += matrix.get(i, j);
        }
    }

    // Output the result
    std::cout << "Sum of matrix elements: " << sum << std::endl;

    return 0;
}
