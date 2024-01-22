def topsis(input_file, weights, impacts, result_file):
    try:
        data = pd.read_csv(input_file)

        if data.shape[1] < 3:
            raise ValueError("Input file does not contain three or more columns.")
        if not data.iloc[:, 1:].apply(np.isreal).all().all():
            raise ValueError("Columns from 2nd to last do not contain numeric values only.")
        if len(weights.split(',')) != len(impacts.split(',')) != data.shape[1] - 1:
            raise ValueError("Number of weights, impacts, and columns must be the same.")
        if not all(impact in ['+', '-'] for impact in impacts.split(',')):
            raise ValueError("Impacts must be either +ve or -ve.")

        norm_data = data.copy()
        for i in range(1, data.shape[1]):
            norm_data.iloc[:, i] = data.iloc[:, i] / np.sqrt(np.sum(data.iloc[:, i]**2))

        weights = np.array([float(weight) for weight in weights.split(',')])
        weighted_norm_data = norm_data.copy()
        for i in range(1, norm_data.shape[1]):
            weighted_norm_data.iloc[:, i] = norm_data.iloc[:, i] * weights[i-1]

        ideal_value = []
        worst_ideal_value = []

        for i in range(1, weighted_norm_data.shape[1]):
            if impacts[i-1] == '+':
                ideal_value.append(weighted_norm_data.iloc[:, i].max())
                worst_ideal_value.append(weighted_norm_data.iloc[:, i].min())
            else:
                ideal_value.append(weighted_norm_data.iloc[:, i].min())
                worst_ideal_value.append(weighted_norm_data.iloc[:, i].max())

        distance_to_ideal = np.sqrt(np.sum((weighted_norm_data.iloc[:, 1:] - ideal_value)**2, axis=1))
        distance_to_worst_ideal = np.sqrt(np.sum((weighted_norm_data.iloc[:, 1:] - worst_ideal_value)**2, axis=1))

        performace_score = distance_to_worst_ideal / (distance_to_ideal + distance_to_worst_ideal)

        result = data.copy()
        result['Topsis Score'] =  performace_score
        result['Rank'] = result['Topsis Score'].rank(ascending=False)

        result.to_csv(result_file, index=False)

        print(f"TOPSIS analysis completed successfully. Results saved to {result_file}")
        
    except FileNotFoundError:
        print("Error: File not found.")



# In[47]:


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python program.py <InputDataFile> <Weights> <Impacts> <ResultFileName>")
    else:
        input_file, weights, impacts, result_file = sys.argv[1:5]
        topsis(input_file, weights, impacts, result_file)

