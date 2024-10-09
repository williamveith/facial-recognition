import numpy as np
import tenseal as ts
import uuid
from pathlib import Path
from pathlib import Path

current_file_path = Path(__file__).resolve()
module_dir = current_file_path.parent
root = module_dir.parent
embeddings_dir_path = module_dir / "embeddings"
encrypted_embed_path = module_dir / "encrypted_embeddings"
magnitudes_file = module_dir / "encrypted_settings/magnitudes.npy"

vectors = [np.load(plaintext_vector) for plaintext_vector in Path(embeddings_dir_path).rglob("*.npy")]
magnitudes = [np.linalg.norm(v) for v in vectors]

# Step 2: Set up TenSEAL context for encryption
context = ts.context(ts.SCHEME_TYPE.CKKS, poly_modulus_degree=8192, coeff_mod_bit_sizes=[40, 20, 40])
context.global_scale = 2**20
context.generate_galois_keys()

# Step 3: Encrypt and save the vectors
for i, vector in enumerate(vectors):
    encrypted_vector = ts.ckks_vector(context, vector)
    encrypted_vector_path = encrypted_embed_path / f'{uuid.uuid4()}.npy'
    encrypted_vector_bytes = encrypted_vector.serialize()
    
    with open(encrypted_vector_path, 'wb') as file:
        file.write(encrypted_vector_bytes)
        
    
if __file__ == "__name__":
    np.save(magnitudes_file, magnitudes)
    with open(encrypted_vector_path, 'wb') as f:
        f.write(encrypted_vector_bytes)

    # Save encryption context (important to load it in Session 2)
    np.save("encrypted_settings/context.tenseal", context)
