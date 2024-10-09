import numpy as np
import tenseal as ts

# Example vectors
vector_A = np.array([1, 2, 3])
vector_B = np.array([4, 5, 6])

# Step 1: Calculate magnitudes (norm) in plaintext
magnitude_A = np.linalg.norm(vector_A)
magnitude_B = np.linalg.norm(vector_B)

# Step 2: Set up TenSEAL context (encryption parameters)
context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[40, 20, 40])
context.global_scale = 2**20
context.generate_galois_keys()

# Step 3: Encrypt the vectors
encrypted_vector_A = ts.ckks_vector(context, vector_A)
encrypted_vector_B = ts.ckks_vector(context, vector_B)

# Save the encrypted vectors to .npy files
encrypted_vector_A.save("encrypted_vector_A.npy")
encrypted_vector_B.save("encrypted_vector_B.npy")

# You can also save the magnitudes in plaintext for later
np.save("magnitude_A.npy", magnitude_A)
np.save("magnitude_B.npy", magnitude_B)

# Now later when we need to compute cosine similarity...

# Step 4: Load the encrypted vectors from the .npy files
encrypted_vector_A = ts.ckks_vector.load(context, "encrypted_vector_A.npy")
encrypted_vector_B = ts.ckks_vector.load(context, "encrypted_vector_B.npy")

# Step 5: Compute the encrypted dot product (A · B)
encrypted_dot_product = encrypted_vector_A.dot(encrypted_vector_B)

# Step 6: Decrypt the result of the dot product
dot_product = encrypted_dot_product.decrypt()

# Step 7: Load the saved plaintext magnitudes
magnitude_A = np.load("magnitude_A.npy")
magnitude_B = np.load("magnitude_B.npy")

# Step 8: Compute the final cosine similarity
cosine_similarity = dot_product / (magnitude_A * magnitude_B)
difference = 1 - cosine_similarity

print(f"Cosine Similarity: {cosine_similarity}")
