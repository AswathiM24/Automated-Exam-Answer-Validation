from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from prettytable import PrettyTable


# Sample original answer uploaded by the examiner and student answers
student_answers = [
    "The array is a data structure where values or items are placed in a linear order, which means the memory assigned to each item is contiguous. The data type of an array is the same for all the elements present in it.With the contiguous memory allocation, it becomes easier to find out the memory location of any element in the array by just knowing the first memory location and adding the offset.",
    "Array is a linear data structure where all elements are arranged sequentially. It is a collection of elements of same data type stored at contiguous memory locations",
    "An array is a data structure that contains a group of elements of the same data type and stores them together in contiguous memory locations.",
    "An array assembles equivalent data elements stored at adjacent memory locations. This easiest data structure helps to determine the location of each piece of data by simply using an offset to the base value. An offset is a number that illustrates the distinction between two index numbers"
]

students_name = [
    "Ajith",
    "Aleena",
    "Amal"
]

def similarity_analysis(model_name, sentences):
    print(f"Using model: {model_name}")
    
    # Load the Sentence Transformer model
    model = SentenceTransformer(model_name)
    # Encode the sentences
    sentence_embeddings = model.encode(sentences)
    
    # Calculate the cosine similarity between the original answer and the student answers
    similarities = cosine_similarity(
        [sentence_embeddings[0]],  # Original answer at zeroth index
        sentence_embeddings[1:]    # Student answers from index 1 onwards
    )

    # # comment this line for benchmarking models
     return similarities[0]

    # Create a pretty table to display names and similarity scores
    t = PrettyTable(['Name', 'Similarity'])
    for name, similarity in zip(students_name, similarities[0]):
        t.add_row([name, round(similarity, 2)])
    return t

# Load a Sentence Transformer model that is suitable for generating sentence embeddings
models = ['paraphrase-multilingual-mpnet-base-v2','all-MiniLM-L12-v2','all-mpnet-base-v2', 'multi-qa-mpnet-base-dot-v1', 'all-distilroberta-v1', 'all-MiniLM-L12-v2',
          'multi-qa-distilbert-cos-v1', 'all-MiniLM-L6-v2', 'multi-qa-MiniLM-L6-cos-v1',
          'paraphrase-albert-small-v2', 'paraphrase-multilingual-MiniLM-L12-v2', 'paraphrase-MiniLM-L3-v2',
          'distiluse-base-multilingual-cased-v1',
          'distiluse-base-multilingual-cased-v2', 'bert-base-nli-mean-tokens','bert-large-nli-mean-tokens']



# Perform the similarity analysis
# The similarity score ranges from 0 to 1, where 1 indicates the highest similarity
# uncomment this for loop for benchmarking models
# for i in models:
#     print(similarity_analysis(i, student_answers))
#     print("\n")
