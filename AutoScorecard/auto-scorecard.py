from src import scorecard

if __name__ == "__main__":
    model, model_table = scorecard.main()
    model_table.to_csv("auto-scorecard-model.csv")
    model.save("model.pkl")
    print(model_table)