import os
import pandas as pd
import random
import warnings
from deap import base, creator, tools, algorithms

def load_data(file_path):
    """Load data from the selected file into a DataFrame."""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith('.xlsx'):
        return pd.read_excel(file_path)
    else:
        raise ValueError("Unsupported file format. Please choose a CSV or Excel file.")

def evaluate(individual, data, unique_targets):
    """Evaluate the fitness of an individual."""
    selected_drugs = [drug for i, drug in enumerate(data['Drug'].unique()) if individual[i] == 1]
    selected_targets = data[data['Drug'].isin(selected_drugs)]['Target'].unique()
    return len(selected_targets),

def run_genetic_algorithm(file_path, num_top_drugs):
    """Run the genetic algorithm to find the top drugs."""
    try:
        data = load_data(file_path)
    except Exception as e:
        print(f"Error loading file: {e}")
        return None, None
    
    if 'Target' not in data.columns or 'Drug' not in data.columns:
        print("The selected file must contain 'Target' and 'Drug' columns.")
        return None, None
    
    unique_targets = len(data['Target'].unique())
    num_drugs = len(data['Drug'].unique())

    random.seed(42)
    
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)
    
    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=num_drugs)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    
    toolbox.register("evaluate", evaluate, data=data, unique_targets=unique_targets)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)
    
    population = toolbox.population(n=300)
    num_generations = 40

    for _ in range(num_generations):
        algorithms.eaSimple(population, toolbox, cxpb=0.5, mutpb=0.2, ngen=1, verbose=False)
    
    top_individuals = tools.selBest(population, k=num_top_drugs)
    
    drug_target_counts = {drug: len(data[data['Drug'] == drug]['Target'].unique()) for drug in data['Drug'].unique()}
    drug_targets = {drug: data[data['Drug'] == drug]['Target'].unique() for drug in data['Drug'].unique()}
    
    selected_drugs = []
    for individual in top_individuals:
        selected_drugs += [data['Drug'].unique()[i] for i in range(num_drugs) if individual[i] == 1]
    
    unique_selected_drugs = list(set(selected_drugs))
    unique_selected_drugs.sort(key=lambda drug: drug_target_counts[drug], reverse=True)
    
    return unique_selected_drugs[:num_top_drugs], drug_targets

def save_results_to_excel(top_drugs, drug_targets, combination_results, filename="results.xlsx"):
    """Save the results of the analysis to an Excel file on the Desktop."""
    if not top_drugs:
        print("No results to save.")
        return
    
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, filename)
    
    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        # Save top drugs
        top_drugs_df = pd.DataFrame({
            'Drug': top_drugs,
            'Targets': [', '.join(drug_targets[drug]) for drug in top_drugs]
        })
        top_drugs_df.to_excel(writer, sheet_name='Top Drugs', index=False)
        
        # Save combination results
        combination_results_df = pd.DataFrame(combination_results, columns=['Drug1', 'Drug2', 'Targets'])
        combination_results_df.to_excel(writer, sheet_name='Potential Combinations', index=False)
    
    print(f"Results saved to {file_path}")

def combination_therapy(file_path, num_top_drugs):
    """Perform combination therapy analysis."""
    top_drugs, drug_targets = run_genetic_algorithm(file_path, num_top_drugs)
    
    if not top_drugs:
        print("No top drugs found. Check your file or parameters.")
        return

    print("Top Drugs:")
    for drug in top_drugs:
        targets = drug_targets[drug]
        print(f"{drug} covers {len(targets)} targets: {', '.join(targets)}")
    
    print("\nPotential Combinations:")
    combination_results = []
    
    for i in range(len(top_drugs) - 1):
        drug1 = top_drugs[i]
        targets1 = drug_targets[drug1]
        for j in range(i + 1, len(top_drugs)):
            drug2 = top_drugs[j]
            targets2 = drug_targets[drug2]
            shared_targets = set(targets1) & set(targets2)
            if shared_targets:
                combination_results.append([drug1, drug2, ', '.join(shared_targets)])
    
    combination_results.sort(key=lambda x: len(x[2].split(',')), reverse=True)
    
    if combination_results:
        for drug1, drug2, shared_targets in combination_results:
            print(f"{drug1} and {drug2} collectively target: {shared_targets}")
        
        # Save results to Excel on Desktop
        save_results_to_excel(top_drugs, drug_targets, combination_results)
    else:
        print("No significant combination found.")

