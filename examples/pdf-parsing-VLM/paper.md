# Verifiable Fully Homomorphic Encryption

## Abstract

Fully Homomorphic Encryption (FHE) is seeing increasing real-world deployment to protect data in use by allowing computation over encrypted data. However, the same malleability that enables homomorphic computations also raises integrity issues, which have so far been mostly overlooked. While FHE's lack of integrity has obvious implications for correctness, it also has severe implications for confidentiality: a malicious server can leverage the lack of integrity to carry out interactive key-recovery attacks. As a result, virtually all FHE schemes and applications assume an honest-but-curious server who does not deviate from the protocol. In practice, however, this assumption is insufficient for a wide range of deployment scenarios. While there has been work that aims to address this gap, these have remained isolated efforts considering only aspects of the overall problem and fail to fully address the needs and characteristics of modern FHE schemes and applications. In this paper, we analyze existing FHE integrity approaches, present attacks that exploit gaps in prior work, and propose a new notion for maliciously-secure verifiable FHE. We then instantiate this new notion with a range of techniques, analyzing them and evaluating their performance in a range of different settings. We highlight their potential but also show where future work on tailored integrity solutions for FHE is still required.

## Introduction

Fully Homomorphic Encryption (FHE), which enables computations on encrypted data, has recently emerged into practice. Thanks to theoretical improvements, and optimizations in both software [1]-[3] and hardware implementations [4]-[6], it is starting to see use in real-world deployments (e.g., the Microsoft Edge Password Monitor [7]). Computing on encrypted data inherently requires malleable ciphertexts (e.g., the addition of two ciphertexts is also valid ciphertext). However, this malleability also raises the issue of integrity, as the server can deviate from the computation requested by the client. This has obvious implications for correctness but can also have more severe consequences: a malicious server can exploit the malleability of FHE to carry out key-recovery attacks [8]-[12], undermining the confidentiality of FHE. So far, most work on FHE schemes and applications has chosen to side-step this issue by making assumptions on the setting and threat model. However, as FHE is starting to be deployed to protect critical information, we must move beyond these assumptions to a threat model that can withstand real-world adversaries.

## Honest-but-Curious Assumption

Historically, the FHE research community has extensively made use of the assumption that the server running an FHE application would be honest-but-curious, rather than actively malicious [13]-[16]. This assumption may be reasonable in some deployment scenarios (e.g., when FHE is used only to ensure regulatory compliance or when dealing with trusted institutions cooperating on their own data). However, the necessity to trust the server to this extent is very limiting to the scope of application scenarios, since a violation of the assumption threatens not only correctness but also confidentiality. In addition, even otherwise trusted parties can be compromised by malicious third parties, exposing this attack surface. While FHE protects against passive attacks, a malicious or compromised server taking part in an FHE application can leverage this to undermine data confidentiality. A class of attacks known as key-recovery attacks exploits the interactive nature of real-world deployments to construct (partial) decryption oracles. These exploit the fact that a server can craft a ciphertext that fails to decrypt correctly for certain secret keys, using the client's reaction or lack thereof as an oracle. Practical key-recovery attacks have been developed for all major FHE schemes [8]-[12]. Therefore, there is an urgent need to strengthen FHE to maintain strong guarantees in the context of these attacks.

## Existing FHE Integrity Approaches

In order to remediate these attacks, a line of research has emerged that constructs more robust FHE schemes [17]-[24] that achieve indistinguishability against chosen ciphertext attacks (IND-CCA1). These schemes remain secure even in the presence of decryption oracles. Unfortunately, many of these constructions assume the presence of cryptographic primitives even stronger than FHE and/or are inefficient to implement in practice. A different line of research focuses on achieving integrity for FHE; guaranteeing a function was correctly executed on the ciphertext while preserving the confidentiality of inputs [25]-[32]. While these are more concretely efficient than the constructions mentioned above, there is a significant gap between the assumptions made by existing work and the way state-of-the-art FHE schemes are used in practice. In particular, existing schemes can only tolerate adversaries limited to verification oracles that are weaker than the decryption oracles present in most real-world settings.

More broadly, the issue of maliciously-secure private computation has also been studied outside the domain of FHE. For example, maliciously-secure secure Multi-Party Computation (MPC) has been studied extensively [33]. However, most techniques do not transfer to the FHE setting since they rely on the interactive nature of MPC.

---



---



---

[26] | Cxt. Maint. | Circuit | Server Inputs | Server Privacy | Approx. FHE | Adversarial Model | Implementation |
[27] | ? | Any | Any | Any | Verif. Oracles | Dec. Oracles | 
[32] | ? | Any | Any | Any | Implementation | 
| EiM [28] | Quadratic | Any | Any | Any | Verif. Oracles | Dec. Oracles | 
| EaM [41] | ? | Any | Any | Any | Verif. Oracles | Dec. Oracles | 
| [29] | LogspaceUnif | Any | Any | Any | Verif. Oracles | Dec. Oracles | 
| [30] | Any | Any | Any | Verif. Oracles | Dec. Oracles | 
| [31] | Any | Any | Verif. Oracles | Dec. Oracles | 
| [42] | Any | Implementation | 

Table 1. Characteristics and Limitations of Existing FHE Integrity Paradigms and Approaches. A ? indicates insufficient details are given while ∘ indicates partial support.

diate values to the circuit so that, for the given input, the circuit results in the output ciphertext. In theory, any generic ZKP system could be used to generate this proof. However, a trivial instantiation would introduce prohibitively large additional overhead in emulating the complex ring operations used in FHE schemes. Recent work has therefore focused instead on developing ZKP systems tailored to FHE.

One line of work uses (homomorphic) hashing to bring the size of FHE ciphertexts down into a range that can be handled more efficiently with ZKP techniques. This includes the first SNARK for FHE presented by Fiore et al. [29] and follow-up work by Bois et al. [30]. However, the homomorphic hashing requirement limits this approach to simple schemes such as the BV scheme [44] which does not feature the complex ciphertext maintenance operations that are necessary to achieve the practical efficiency enjoyed by state-of-the-art FHE schemes. An alternative approach by Ganesh et al. [31] instead focuses on constructing a generic ZKP system that natively operates on the rings used in FHE schemes. This drastically improves the efficiency of proving the ring operations that make up basic homomorphic operations such as addition and multiplication. However, ciphertext-maintenance operations generally require either switching between different rings or non-ring operations such as rounding, which are not supported by the current construction. While such tailored approaches hold the promise of significant performance improvements, they cannot currently support efficient modern state-of-the-art FHE schemes. Therefore, when we consider FHE integrity in practice in Section 5, we will focus on generic ZKP systems and discuss how to efficiently instantiate it for FHE.

**Trusted Execution Environment Attestation.** Trusted Execution Environments (TEEs) such as Intel SGX [38] can be used to provide confidentiality, but a series of attacks [45], [46] has put their suitability for this task in question. However, their integrity protections, i.e., their ability to attest to the program running in the enclave, have so far mostly resisted practical attacks [47]. Therefore, it is natural to augment the confidentiality properties of FHE with the integrity protections of TEEs by running FHE inside an enclave. However, the computational complexity of FHE and especially the large sizes of ciphertexts and evaluation keys pose a challenge to TEEs, which are usually more restricted in terms of memory and available computational power than the underlying untrusted hardware. More fundamentally, they can only be employed in settings where the additional trust assumption on the specific hardware vendor is acceptable. Natarajan et al. [42] present an FEE-in-TEE design and implementation, that, because of the ability of TEEs to express arbitrary computations, can easily support modern state-of-the-art FHE schemes with little to no required modifications.

In this section, we consider to what extent the assumptions and guarantees proposed in the existing FHE integrity literature fulfill the requirements of real-world FHE deployments. We highlight the differences between the deployment settings assumed by the existing literature and the needs of real-world FHE deployments, uncovering significant mismatches. In the following (Sections 3.3 and 3.4), we discuss the implications of this mismatch for correctness and confidentiality.

**FHE Deployment Settings.** The existing literature on FHE integrity assumes the outsourced computation setting, where a client provides an encrypted input x and a function (or circuit) f to the server, which then computes f(x) homomorphically and returns the encrypted result. While this setting is the most natural to define FHE in, it is not the only setting or even the most widespread one. In practice, the server has the ability to both choose the circuit to compute and to provide additional inputs. This opens up a variety of important additional use cases that enable a form of two-party computation. For example, this can be used to offer privacy-preserving Machine Learning as a Service (MLaaS) where the server has a model that it wants to make available as a service and the client wants to receive a homomorphically computed inference on its private input [48]–[50]. More generally, we can categorize different types of FHE deployment by the aspects that must remain private. We assume that the client always has some secret inputs, but beyond that, we distinguish between settings with no server input, public (server) inputs, or private server inputs. We can also distinguish between settings with a public circuit f and settings where the circuit is private to either the client or server.

**3.2. FHE Integrity in Practice**

---



---



---

**4.1. Defining Maliciously-Secure Verifiable FHE**

One of the key insights of our notion is that we consider a stronger and arguably more realistic threat model. Existing notions result in an inconsistent view of the server, which is both expected to deviate from the computation (otherwise, integrity notions would not be necessary) yet, at the same time, assumes that the server will not use these deviations to exploit common decryption (failure) oracles that arise in real-world FHE to undermine confidentiality. This can result in a false sense of security, leading users of constructions achieving these notions to believe that they have stronger protections than these notions in fact offer. Because of this inconsistency, we believe that the natural threat model beyond the semi-honest server assumption should be an actively malicious server with full access to a decryption oracle. In addition, we also consider an unbounded verification oracle in order to give similar strength to the integrity guarantees.

While there is a natural definition for confidentiality in this threat model (i.e., IND-CCA1 security²), extending existing FHE integrity notions with this guarantee is non-trivial because these notions interleave aspects of integrity and confidentiality. As a result, formalizing the interactions that arise between these (and their oracles) would be challenging and prone to errors. For example, we split correctness (Dec(Enc(m)) = m) and completeness (i.e., verifiability) which are usually combined in existing notions. This allows us to reason about constructions more cleanly, and also allows us to easily define extensions of our core notion. For example, we are the first to extend integrity notions to approximately FHE [55], where correctness holds only approximately (Dec(Enc(m)) ≈ m). Because we split correctness and completeness, changing between verifiable FHE and verifiable approximate FHE has no knock-on-effects on the remainder of the notion. For space reasons, we present the exact notion of correctness here and refer to Appendix A for a discussion of the approximate notion.

**Definition 4.1 (Maliciously-Secure Verifiable FHE)**

A maliciously-secure verifiable FHE (vFHE) scheme is a tuple (KGen, Enc, Eval, Verify, Dec) of PPT algorithms:

*   KGen(1^f) → (pk, sk)
*   Enc_k(y) → (c_x, τ_x) where key is either^3 pk or sk
*   Eval_pk(c_x) → (c_y, τ_y) where y = f(x)
*   Verify_sk(c_y, τ_y) → b, the client accepts if b = 1 and rejects otherwise

FHE cannot achieve IND-CCA2 by its nature.

When key is pk, the scheme achieves public delegatability, which is natural for FHE since all modern schemes offer public-key encryption.

The scheme must satisfy the correctness, completeness, soundness, and security properties defined below in the context of our adversary model.

Note that this notion already supports public inputs on the server, modeling them as part of the function f. We discuss how to extend it to support private server inputs in the next section. Note also that f is public by default, and we discuss how to extend this notion to support circuit privacy in a following section. We present our notion with designated verifiability, i.e., some secret key material might be required to verify a ciphertext. We believe that this natural for the FHE setting, where only the secret key holder can decrypt a ciphertext and therefore has any benefit from verifying it. However, our notion can be trivially adapted to public verifiability if desired. Note that even in a threshold FHE or multi-key FHE setting, designated verifiability is sufficient, since the key holders can extend the MPC protocol they run to decrypt to also realize verification.

**Adversary Model.** We assume a PPT adversary with access to an unbounded verification and decryption oracle O_Dec(c_x, τ_y, τ_z) := b which returns b = 1 if Verify_kpk(c_x, τ_y, τ_z) = 0, and b = Dec_sk(c_x) otherwise^4. In addition, the adversary has access to the usual encryption oracle O_Enc which we omit for brevity.

**Definition 4.2 (Correctness)**

A scheme is correct if any honest computation will decrypt to the expected result. More formally, a scheme is correct if for all functions f, and for all x in the domain of f:

Pr[Dec_sk(c_y) = f(x) | (pk, sk) ← KGen(1^f), c_x, τ_x) ← Enc_kpk(x), c_y, τ_y) ← Eval_pk(c_x)]

**Definition 4.3 (Completeness)**

A scheme is complete if Verify will always accept can honestly computed result. More formally, a scheme is complete if for all functions f, and for all x in the domain of f:

Pr[Verify_sk(c_y, τ_y) = 1 | (pk, sk) ← KGen(1^f), c_x, τ_x) ← Enc_kpk(x), c_y, τ_y) ← Eval_pk(c_x)]

**Definition 4.4 (Soundness)**

A scheme is sound if the adversary cannot make Verify accept an incorrect answer. Formally, a scheme is sound if for any PPT adversary A and any function f the following probability is negligible in the security parameter A:

Pr[Verify_sk(c_y, τ_y) = 1 | (pk, sk) ← KGen(1^f), c_x, τ_x) ← A^O_Dec(c_x, τ_y) | c_y, τ_y) ← Enc_kpk(c_x), f(x)]

---

Definition 4.5 (Security)
==========================

We extend the definition of IND-CCA1 to our notion. Note that we do not require an evaluation oracle since Evalpk is public and can be executed by the adversary directly. Formally, a scheme is secure if for any PPT adversary A and any function f the advantage AdvIND-CCA1[A] (λ) = 2|Pr[b = 0] - 1/2 of the attacker in the following game is negligible in the security parameter λ:

IND-CCA1 for vFHE

(pk, sk) ← KGen(1^f)

(m0, m1)^(1^f, pk)

(c^*, τ*) ← Encpk(mb)

b ← A^(c*)

Verifiable FHE is defined in Definition 4.1 addresses key-recovery attacks and ensures that client inputs are protected as expected. However, it does not address the privacy of server inputs and we therefore provide an extension of the notion which can be used in settings where formal guarantees for server privacy are required. In the existing FHE literature, the notion of circuit privacy addresses both the privacy of the function and any server inputs. It requires that the result of a computation is indistinguishable from a fresh encryption (with the same parameters). However, this is a stronger guarantee than what we require here since we address circuit privacy as a separate property in the next section. In addition, the traditional definition might be hard to achieve in practice, given that the integrity tags 7 of a fresh encryption and a computation output might be substantially different, making distinguishing them trivial.

We instead define our notion as vFHE plus a new property we term "Server Privacy". Informally speaking, it requires that the result of an evaluation reveals nothing to the client beyond the output of the function. Existing work that considers hiding server inputs does not explicitly state the threat model for this setting. We address this issue and define an adversary model that considers the client as the adversary. For example, considering the perspective of the client, the indistinguishability has to hold even when the adversary has access to the secret key. In addition, we must assume that the client generates keys and encrypts honestly, i.e., we assume a semi-honest client. We could strengthen the threat model at the cost of requiring proofs of correct key generation and encryption. However, we believe that this would be prohibitively expensive and not appropriate for most settings. We note the parallels between this setting and generic 2-Party MPC. However, in MPC, parties usually have equal protection. Here, the guarantee offered to the client is stronger, since the server never learns the output of the function and therefore has no information on the client input, not even that which would be derivable from the function output.

Definition 4.6 (vFHE with Server Privacy)

A maliciously-secure verifiable FHE scheme with server privacy is a tuple (KGen, Enc, Verify, Dec, Eval) of PPT algorithms:

    * KGen, Enc, Verify, Dec are defined as in Definition 4.1,

    * Evalpk(cx, w) → cy, ry where y = f(x, w)

The scheme must satisfy (slightly modified versions of) the correctness, completeness, soundness, and security properties defined above:

    * For correctness (Definition 4.2) and completeness (Definition 4.3) only trivial syntactic changes to accommodate the modified Eval are required.

    * For soundness (Definition 4.4), Decsk(cy) ≠ f(x) is replaced by 7w s.t. Decsk(cy) = f(x, w). Informally, this means that if Verify accepts, then there exists at least one set of private server inputs that satisfies the circuit.

    * The definition of security (Definition 4.5) remains unchanged, but the scheme must additionally satisfy the server privacy property defined below.

Definition 4.7 (Server Privacy)

Informally, a scheme offers server privacy when Eval reveals nothing about the server inputs beyond what can be learned from the output. We assume a semi-honest PPT adversary with access to all keys, including sk. Formally, a scheme offers server privacy when the following are (statistically indistinguishable for all w, w'):

(f(x, w), Evalpk(cx, w)) ≈ (f(x, w'), Evalpk(cx, w'))

Definition 4.8 (Circuit Privacy)

When considering circuit privacy, there are two natural versions of this property: We can have either the server or the client provide the (private) circuit. While applications relying on this are currently rare in practice, certain critical applications could require formal guarantees of this nature. While the FHE literature has defined the notion of circuit privacy from the very beginning, existing integrity notions generally did not consider this aspect. This seems initially justified in the case of a server-provided circuit since the resulting correctness guarantees are essentially meaningless. However, this is only true when ignoring decryption oracles (as existing notions do). In the presence of decryption oracles, it remains meaningful to ensure the well-formedness of ciphertexts to prevent key-recovery attacks. Client-provided circuit privacy, on the other hand, does not have a correspondence in the traditional FHE literature, nor has it appeared in existing integrity notions. However, of the two, it is arguably the more interesting in the context of integrity since one can extend the privacy guarantees to the circuit while maintaining the same strong correctness guarantees. Because our notion separates the concepts of server input privacy and circuit privacy, we can easily define both client and server versions of the latter. Both are very similar and, in the following, we define circuit privacy only from the perspective of the client and refer to Appendix A for the.

---



---

**page 10 of academic paper**

**Construction 1 (vFHE with Private Server Input)**

* Let $\mathcal{E} = \mathcal{E}.KGen, \mathcal{E}.Enc, \mathcal{E}.Dec, \mathcal{E}.Eval$ be an IND-CPA secure FHE scheme with (FHE) circuit privacy (See Appendix A for formal definitions).
* Let $\mathcal{F}_{X,W}$ be a set of functions, with $f \in F$ if for all $x \in X$ and $w \in \mathcal{W}, \mathcal{E}.Dec_{\mathcal{E}.sk}(f \in F \text{ if for all } x \in X \text{ and } w \in \mathcal{W} \text{ results in a valid plaintext}^{5})$ (which can be a subset of all possible plaintext).
* Let $\Pi = (\Pi.KGen, \Pi.Prove, \Pi.Verify)$ be a generic zero-knowledge proof (e.g., a zkSNARK) for $ZKPPoK \{w : c_y = \mathcal{E}.Eval_{\mathcal{E}}(f, c_x, w) \wedge w \in \mathcal{W}\}$.

For $f \in F$, we construct a vFHE scheme with private server inputs (KGen, Enc, Eval, Verify, Dec) satisfying Definition 4.6 from these building blocks as follows:

    * $KGen(1^{k}, f) \rightarrow ((c_{E}, pk_{\Pi}), (sk_{E}, sk_{\Pi}))$, where $(pk_{E}, sk_{E}) = \mathcal{E}.KGen(1^{k})$ and $(pk_{\Pi}, sk_{\Pi}) = \Pi.KGen(1^{k})$
    * $Enc_{pk}(x) \rightarrow (c_{x}, \tau_{x})$, where $\tau_{x} = c_{x}$ and $c_{x} = (\mathcal{E}.Enc_{pk_{E}}(x))$
    * $Eval_{pk}(c_x, w) \rightarrow (c_y, \tau_y)$, where $c_y = \mathcal{E}.Eval(f, c_x, w)$ and $\tau_y = \Pi.Prove(c_y, \tau_x, w)$
    * Verify_{pk}(c_y, \tau_y) = \Pi.Verify(\tau_y, \tau_x, w)
    * $Dec_{sk}(c_y) \rightarrow y, where $y = \mathcal{E}.Dec_{sk_{E}}(c_y)$

Proof

The correctness of our construction reduces to the correctness of the FHE scheme, and the completeness reduces to the completeness of the ZKP scheme. Security can be reduced to the semantic security of the FHE scheme (because we assume $f \in F_{X,W}$ and enforce $w \in W$ and correct execution through the ZKP, and $x \in X$ in the encryption). Soundness follows directly from the soundness of the ZKP, while server privacy is achieved via the circuit privacy (as defined in FHE) of the FHE scheme and through the zero-knowledge property of the ZKP. We refer to the extended version of this paper [57] for a more formal proof.

5. Instantiating Verifiable FHE in Practice

In this section, we instantiate our notion of maliciously-secure verifiable FHE using state-of-the-art FHE and ZKP schemes. We highlight a series of challenges in bringing together modern FHE and ZKP systems, including the mismatch between the large polynomial rings used in most state-of-the-art FHE schemes and the integer fields used in the vast majority of ZKP systems. We investigate several approaches to bridge this gap and introduce a new optimization for emulating ring arithmetic inside ZKPs.

We consider a wide range of ZKP systems and identify four promising candidates that are best suited to the characteristics of FHE verification. In addition, we also discuss how to instantiate our notion with hardware attestation primitives, introducing an optimization that allows us to accelerate FHE-in-TEE by a factor of two over the existing state-of-the-art for multiplications. We evaluate our ZKP- and TEE-based instantiations for a variety of different workloads going far beyond the type of circuits that existing FHE integrity notions can express.

5.1. Verifiable FHE via ZKP

In the following, we discuss how to instantiate our construction for verifiable FHE with private server inputs (c.f. Section 4.5).

Bridging FHE and ZKP. The areas of FHE and ZKP have been maturing mostly independently, and state-of-the-art ZKP systems have primarily been tailored to applications that share few characteristics with FHE. In addition, FHE computations are inherently large and complex, making proofs non-trivial. Most of this complexity arises from the advanced ciphertext maintenance operations used by state-of-the-art schemes. As a result, previous work on FHE integrity frequently chose to use simple schemes such as the BV scheme [44] to avoid this complexity. However, the applicability of these schemes is limited in practice because of their prohibitive overhead. We instead choose to target modern state-of-the-art FHE schemes which offer the performance necessary to realize real-world FHE applications. FHE schemes fall into two main families, with the LWE-based FHEW [16] and TFHE [15] schemes focusing primarily on evaluating binary circuits, while RLWE-based schemes such as BGV [14], B/FV [58] [13] and CKKS [55]) focus on arithmetic circuits. Initially, LWE-based schemes might appear promising since they use smaller ciphertexts and offer faster computation. However, efficient implementations of schemes in this family usually make heavy use of floating-point operations, which would introduce significant overhead in the ZKP proofs. The RLWE schemes, in turn, feature larger ciphertexts but also offer a powerful form of data parallelism [59] that is at the core of most state-of-the-art FHE results. While our construction can be instantiated with any scheme, we select BGV because it is amenable to integer-based ZKP and requires the least amount of non-arithmetic operations to realize its ciphertext-maintenance operations.

The RLWE setting introduces a fundamental mismatch between the ring based FHE computation and the mostly field based ZKP systems. Specifically, BGV uses rings of the form $R_{q} = \mathbb{Z}_{q}[X] / (X^{n}+1)$, i.e. polynomials with degree $n$.

---



---

[64] candidate for realization using STARKs. Recent work can also forge explicit arithmetization and instead directly express arithmetic circuits. However, this approach scales poorly with the number of inputs, which is high for FHE circuits due to the expansion from individual ciphertexts to 2N field elements (where N = 2^13). As a result, RICS currently remains the most appropriate choice for FHE integrity applications, and we consider only ZKP systems with efficient support for RICS arithmetizations.

ZKP Scheme Selection. In recent years, a large variety of efficient ZKP systems has been proposed, with many seeing widespread use in real-world deployments. However, when selecting suitable candidates for our instantiation, we need to consider that FHE has slightly different requirements than, e.g., blockchain applications. For example, due to the large ciphertext expansion, proof size is less of a concern in FHE, which already introduces a noticeable communication overhead. Instead, we are mostly concerned with achieving a good trade-off between prover and verifier time. Note that we do not require public verifiability and can therefore exploit potentially more efficient designated verifiability schemes. We select four candidate approaches that are especially suitable for verifiable FHE:

First, we consider Groth16 [65], which represented a major breakthrough in practical ZKP research, showing that zkSNARKs can be achieved with good concrete efficiency. It requires a trusted setup, which presents difficulties in settings where the set of parties is not known in advance, such as in blockchain applications. However, in verifiable FHE, the client and server can easily realize this trusted party during a one-time setup via a 2-party maliciously-secure MPC protocol. Follow-up work has introduced new schemes with different tradeoffs, such as removing the need to re-run the setup for each circuit. However, this is not relevant to FHE, where parameters are usually already circuit-specific. On the other hand, we do evaluate transparent SNARKs that completely remove the need for such a set-up. Here, we consider Bulletproofs [66] which is part of a generation of zkSNARKs without trusted setup that brings them into the same realm of performance as traditional efficient constructions that require (universal or per-circuit) setup. While most implementations of Bulletproofs focus on using it for most implementations of Bulletproofs focus on using it for efficient range proofs, for FHE we also require the ability to support more generic R1CS systems. We also evaluate Aurora [67], which is part of the same generation and trades off asymptotically worse prover times and proof sizes for a move to post-quantum secure assumptions, which matches nicely with the post-quantum security of FHE schemes.

Finally, we also consider Rinoctho [31] by Ganesh et al., which briefly discussed in Section 3.1. Rinoctho offers native support for FHE-friendly rings, potentially giving significant performance benefits over systems that need to emulate these rings. We extend Rinoctho with a more optimized encoding scheme but, for brevity, refer to Appendix C for further details on our optimization. However, its expressiveness is limited, as Rinoctho only supports arithmetic ring operations, whereas some FHE operations (e.g., relinearization) use component-wise rounding operations internally. Additionally, Rinoctho only provides only around 60 bits of (computational) soundness for the rings used in FHE. We use a simple soundness amplification strategy, running three separate instances of the protocol to achieve stronger soundness guarantees. Overall, Rinoctho is much more FHE-friendly than previous proof or argument systems, but still struggles to efficiently represent state-of-the-art FHE optimizations natively. Nevertheless, we include it because it represents an interesting avenue for future work and promises significantly improved performance for the circuits it can support. In Section 5.3, we evaluate our construction when instantiated using these ZKP schemes and also compare it against a TEE-based instantiation.

**5.2. Verifiable FHE via TEE**

In this instantiation, we use hardware attestation rather than cryptographic proofs to provide the integrity component. We note that, while there has been a plethora of attacks on TEE-based confidentiality guarantees [45]-[47], there have been significantly fewer issues with the attestation-based integrity guarantees [47]. Natarajan et al. presented the first implementation of this FHE-in-TEE approach [42] and we extend their work to our notion with server inputs. In addition, we introduce an optimization that allows us to efficiently compute subfunctions on untrusted hardware. Since TEEs can directly attest to the program that they are running, there is no need for explicit arithmetization. However, programs will frequently require adjustments to properly interface with the enclave SDK and to remove unsupported operations and performance bottlenecks. Nevertheless, TEEs support most FHE schemes more naturally than ZKP systems, including offering native support for, e.g., rounding or floating-point operations. However, computations and especially memory operations inside the enclave are significantly slower than operations in the untrusted domain. We address this issue partially by introducing a new optimization that accelerates FHE-in-TEE by a factor of two for batched multiplications. The key insight in our optimization is that the server can also rely on the guarantees of the enclave to not leak its inputs to the client. Specifically, it can use lightweight cryptographic proofs that do not have the zero-knowledge property to prove the enclave that computations performed on the untrusted hardware are indeed correct and can be relied upon by the enclave. This enables our optimization which computes computationally expensive batched multiplications on untrusted hardware and then uses an efficient Schwartz-Zippel-based proof of correctness to move them back to the trusted domain. For brevity, we refer to Appendix D for a detailed description.

**5.3. Performance Analysis**

In this section, we evaluate our ZKP- and TEE-based instantiations across a range of workloads representing different levels of complexity. We conclude our analysis with a brief outlook on the future of FHE integrity.

---

# Performance Results for Different Instantiations of Verifiable Fully Homomorphic Encryption.

Table 2. Performance Results for Different Instantiations of Verifiable Fully Homomorphic Encryption.

For FHE, Setup = Key Generation, Prover = Homomorphic Computation and Verifier = Encryption/Decryption

**Implementation & Setup.**

We use the Microsoft SEAL [2] implementation of the BGV scheme [14], which is a state-of-the-art RNS- and NTT-based implementation. We express our ZKP circuits using Circom [68] which translates its custom specification language to R1CS. We rely on a variety of state-of-the-art ZKP implementations for the backends: we use the arkworks library [69] to implement Groth16 [65], for Aurora [67] we use the libiop library by the same authors, and for Bulletproofs [66] we use the Dalek library [70]. We implement Rinocchio [31] and extend it with an optimized encoding scheme (cf. Appendix C). We make our implementation available as open-source [8]. For the TFE-based approach, we re-implement CHEX-MIX [42] and extend it with our optimization (cf. Appendix D), targeting Intel SGX via the OpenEnclave SDK [71]. We make our FHE-in-TEE framework available as open-source [9]. We evaluate our implementations on an AWS c5d. 4xlarge instance with 16 vCPUs and 32 GB of RAM. We make our instantiations and evaluation setup publicly available [10].

**Workloads.**

We consider three different circuits, each representing a different level of complexity: (i) Our Toy circuit computes a ciphertext-ciphertext multiplication (tensoring only, no post-processing) on two inputs provided by the client, i.e., in the outsourced computation setting considered by previous work. (ii) The Small circuit represents a more realistic low-depth two-party computation, computing NoiseFlood(x·w+w) for an encrypted client input x and private server inputs w and w (here, both arithmetic operations are ciphertext-plaintext operations). The presence of the server inputs requires input checks to ensure validity and prevent key-recovery attacks. Their private nature requires performing and proving noise-flooding as part of the 'computation. We follow the approach described in [30], which adds randomly-selected encryptions of zero to increase the noise of the ciphertext without modifying the message. Finally, our Medium circuit introduces ciphertext-maintenance operations, computing NoiseFlood(ModSwitch((x-w)²) for a client input x and a private server input w. As in the previous task, this requires proving the validity of the client input and ensuring server privacy via noise-flooding. In addition, it requires computing and proving the modulus switching ciphertext operation, going well beyond what prior work on FHE integrity is able to express.

**Performance.** In Table 2 we present the performance results for the different instantiations, compared against a baseline of non-verified FHE. The FHE parameters for the workload are N = 8192 and log₂q = 137 = 45 + 46 + 46, and the zero-knowledge proofs have between 2²² and 2²⁴ R1CS constraints. We observe that the runtimes fall into three different categories: practical (seconds), acceptable (minutes), and impractical (hours). We note that verifier times are always either practical or at least acceptable. However, prover time varies wildly between the different instantiations. For example, transparent SNARKs (Bulletproofs and Aurora) take several hours to compute the proofs. In addition, they have the slowest verifier times, making them overall unattractive for FHE verification, especially when considering that FHE permits a straightforward realization of trusted setups. Groth16 offers the best verification time, being nearly indistinguishable from pure FHE. At the same time, it offers acceptable prover runtimes in the order of minutes. This comes at the cost of several minutes of trusted setup, but that can be amortized over many client queries. Rinocchio (implemented with our optimizations) offers slightly slower but still very practical client verification but improves significantly on prover time and especially setup times. Finally, FHE-in-TEE offers by far the most practical performance at the cost of additional trust assumptions and hardware requirements.

**Outlook.** Our work shows that, while the cost of robustness is clearly non-negligible, it is, today, already acceptable for high-value applications in challenging settings. FHE applications currently mostly focus on settings where latency is not critical, which allows them to tolerate the additional overhead more easily. While our constructions and instantiations explored (and optimized) existing state-of-the-art FHE and ZKP schemes, there are further opportunities to improve performance through the co-design of FHE and ZKP schemes. More fundamentally, we need to improve our understanding of how to construct efficient and expressive ring-native ZKP systems. We believe that the increasing demand to deploy FHE in challenging real-world environments will also drive future research on these issues.

**Acknowledgments.** We would like to thank Chaya Ganesh, Anca Nitulescu, Eduardo Soria-Vazquez, Michael Steiner, Nojan Sheybani, Erin Hales, Lea Nüberger, Martha Norberg Hovd, and the PPS Lab team for their insightful input and feedback. We would also like to acknowledge our sponsors for their generous support, including Meta, Google, SNSF through an Ambizione Grant No. 186050, and the Semiconductor Research Corporation.

The end.

---

**References**

[1] S. Halevi and V. Shoup, "Algorithms in HElib," in Advances in Cryptology - CRYPTO 2014, pp. 554–571, Springer Berlin Heidelberg, 2014.

[2] H. Chen, K. Laine, and R. Player, "Simple encrypted arithmetic library - SEAL v2.1," in Financial Cryptography and Data Security, pp. 3–18, Springer International Publishing, 2017.

[3] A. Al Badawi, J. Bates, Fchi, D. B. Cousins, S. Erabelli, N. Genise, S. Halevi, H. Hunt, A. Kim, Y. Lee, Z. Liu, D. Micciancio, I. Quah, Y. Polyakov, S. R.V., K. Roblff, J. Saylor, D. Svonitsky, M. Triplett, V. Vaikuntanathan, and V. Zucca, "OpenFHE: Open-Source fully homomorphic encryption library," in Proceedings of the 10th Workshop on Encrypted Computing & Applied Homomorphic Cryptography, WAHC'22, (New York, NY, USA), pp. 53–63, Association for Computing Machinery, 7 Nov. 2022.

[4] N. Samardzic, A. Feldmann, A. Krstev, S. Devadas, R. Dreslinski, C. Peikert, and D. Sanchez, "FI: A fast and programmable accelerator for fully homomorphic encryption," in MICRO-54: 54th Annual IEEE/ACM International Symposium on Microarchitecture, MICRO '21. (New York, NY, USA), pp. 238–252, Association for Computing Machinery, Oct. 2021.

[5] R. Geelen, M. Van Beirendonck, H. V. L. Pereira, B. Huffman, T. McAuley, B. Selfridge, D. Wagner, G. Dimou, I. Verhauwhele, F. Veraaurenen, and D. W. Archer, "BASALISC: Flexible asynchronous hardware accelerator for fully homomorphic encryption," 27 May 2022.

[6] A. Feldmann, N. Samardzic, A. Krstev, S. Devadas, R. Dreslinski, K. Elfrawy, N. Genise, C. Peikert, and D. Sanchez, "FI: A fast and programmable accelerator for fully homomorphic encryption (extended version)," 11 Sept. 2021.

[7] K. Laufer, S. Kannepalli, K. Laine, and R. C. Moreno, "Password monitor: Safeguarding passwords in Microsoft edge," 2021.

[8] P. Fauzi, M. N. Heyd, and H. Raddum, "On the IND-CCA1 security of FHE schemes," Cryptology ePrint Archive, 2021.

[9] Z. Zhang, T. Plantard, and W. Susilo, "Reaction attack on outsourced computing with fully homomorphic encryption schemes," in Information Security and Cryptology - ICISC 2011, pp. 419–436, Springer Berlin Heidelberg, 2012.

[10] I. Chillotti, N. Gama, and L. Goubin, "Attacking FHE-based applications by software fault injections," Cryptology ePrint Archive, 2016.

[11] M. Chenal and Q. Tang, "On key recovery attacks against existing somewhat homomorphic encryption schemes," in Progress in Cryptology - LATINCRYPT 2014, pp. 239–258, Springer International Publishing, 2015.

[12] B. Chaturvedi, A. Chakraborty, A. Chatterjee, and D. Mukhopadhyay, "A practical full key recovery attack on THE and FHEW by inducing decryption errors," Cryptology ePrint Archive, 2022.

[13] J. Fan and F. Veraaurenen, "Somewhat practical fully homomorphic encryption," Cryptology ePrint Archive, 2012.

[14] Z. Brakerski, C. Gentry, and V. Vaikuntanathan, "leveled fully homomorphic encryption without bootstrapping," ACM Trans. Comput. Theory, vol. 6, pp. 1–36, July 2014.

[15] I. Chillotti, N. Gama, M. Georgieva, and M. Izabachene, "TFHE: Fast fully homomorphic encryption over the torus," J. Cryptology, vol. 33, pp. 34–91, Jan. 2020.

[16] L. Ducas and D. Micciancio, "FHEW: Bootstrapping homomorphic encryption in less than a second," in Advances in Cryptology - EUROCRYPT 2015, pp. 617–640, Springer Berlin Heidelberg, 2015.

[17] D. Boneh, R. Canetti, S. Halevi, and J. Katz, "Chosen-Ciphertext security from Identity-Based encryption," SIAM J. Comput., vol. 36, pp. 1301–1328, Jan. 2007.

[18] J. Loftus, A. May, N. P. Smart, and F. Veraaurenen, "On CCA-Secure somewhat homomorphic encryption," in Selected Areas in Cryptography, pp. 55–72, Springer Berlin Heidelberg, 2012.

[19] Z. Li, S. D. Galbraith, and C. Ma, "Preventing adaptive key recovery attacks on the GSW levelled homomorphic encryption scheme," in Provably Security, pp. 373–383, Springer International Publishing, 2016.

[20] J. Lai, R. H. Deng, C. Ma, K. Sakurai, and J. Weng, "CCA-Secure Keyed-Fully homomorphic encryption," in Public-Key Cryptography - PKC 2016, pp. 70–98, Springer Berlin Heidelberg, 2016.

[21] K. Emura, G. Hanaoka, K. Nuida, G. Ohtake, T. Matsuda, and S. Yamada, "Chosen ciphertext secure keyed-homomorphic public-key cryptosystems," Des. Codes Cryptogr., vol. 86, pp. 1623–1683, Aug. 2018.

[22] B. Wang, X. Wang, and R. Xue, "CCA1 secure FHE from PIO, revisited," Cybersecurity, vol. 1, pp. 1–8, Sept. 2018.

[23] K. Emura, "On the security of Keyed-Homomorphic PKEs: Preventing key recovery attacks and ciphertext validity attacks," IEICE Transactions on Fundamentals of Electronics, Communications and Computer Sciences, vol. E104.A, no. 1, pp. 310–314, 2021.

[24] S. Sato, K. Emura, and A. Takayasu, "Keyed-Fully homomorphic encryption without indistinguishability obfuscation," Cryptology ePrint Archive, 2022.

[25] R. Gennaro, C. Gentry, and B. Parno, "Non-interactive verifiable computing: Outsourcing computation to untrusted workers," in Advances in Cryptology - CRYPTO 2010, pp. 465–482, Springer Berlin Heidelberg, 2010.

[26] R. Gennaro and D. Wichs, "Fully homomorphic message authenticators," in Advances in Cryptology - ASIACRYPT 2013, pp. 301–320, Springer Berlin Heidelberg, 2013.

[27] D. Catalano and D. Fiore, "Practical homomorphic MACs for arithmetic circuits," in Advances in Cryptology - EUROCRYPT 2013, pp. 336–352, Springer Berlin Heidelberg, 2013.

[28] D. Fiore, R. Gennaro, and V. Pastro, "Efficiently verifiable computation on encrypted data," in Proceedings of the 2014 ACM SIGSAC Conference on Computer and Communications Security, CCS '14, (New York, NY, USA), pp. 844–855, Association for Computing Machinery, Nov. 2014.

[29] D. Fiore, A. Nitulescu, and D. Pointcheval, "Boosting verifiable computation on encrypted data," in Public-Key Cryptography - PKC 2020, pp. 124–154, Springer International Publishing, 2020.

[30] A. Bois, I. Cascudo, D. Fiore, and D. Kim, "Flexible and efficient verifiable computation on encrypted data," in Public-Key Cryptography - PKC 2021, pp. 528–558, Springer International Publishing, 2021.

[31] C. Ganesh, A. Nitulescu, and E. Soria-Vazquez, "Rinocho: SNARKs for ring arithmetic," Cryptology ePrint Archive, 2021.

[32] S. Chakel, C. Knabenhans, A. Pyrgelis, and J.-P. Hubaux, "Verifiable encodings for secure homomorphic analytics," July 2022.

[33] D. Evans, V. Kolesnikov, and M. Rosulek, "A pragmatic introduction to secure Multi-Party computation," Foundations and Trends® in Privacy and Security, vol. 2, no. 2-3, pp. 70–246, 2018.

[34] S. Goldwasser, Y. T. Kalai, R. A. Popa, V. Vaikuntanathan, and N. Zeldovich, "How to run Turing machines on encrypted data," in Advances in Cryptology - CRYPTO 2013, pp. 536–553, Springer Berlin Heidelberg, 2013.

[35] C. Gentry, "A fully homomorphic encryption scheme," PhD thesis, Stanford University, 2009.

[36] O. Regev, "On lattices, learning with errors, random linear codes, and cryptography," Journal of the ACM, vol. 56, pp. 34:1–34:40, Sept. 2009.

---

[37] V. Lyubashevsky, C. Peikert, and O. Regev, "On ideal lattices and learning with errors over rings," in Advances in Cryptology - EU-ROCRYPT 2010, (Berlin Heidelberg, Berlin, Germany), pp. 1–23, Springer Berlin Heidelberg, 2010.

[38] "Intel® software guard extensions (intel® SGX)," https://www.intel.com/content/www/us/en/architecture-and-technology/software-guard-extensions.html. Accessed: 2022-11-2.

[39] J. Geater, "ARM Trust in Trusted Computing for Embedded Systems (B. C. N. Cardaele, D. Soudris, and I. Anagnostopoulos, eds.), pp. 35–45, Cham: Springer International Publishing, 2015.

[40] "AMD SEV-SNP: Strengthening VM isolation with integrity protection and more," https://www.amd.com/system/files/TechDocs/SEV-SNP-strengthening-vm-isolation-with-integrity-protection-and-more.pdf.

[41] S. Li, X. Wang, and R. Zhang, "Privacy-Preserving homomorphic MACs with efficient verification," in Web Services - ICWS 2018, pp. 100–115, Springer International Publishing, 2018.

[42] D. Natarajan, A. Loveless, W. Dai, and R. Dreslinski, "CHEX-MIX: Combining homomorphic encryption with trusted execution environments for two-party oblivious inference in the cloud," Cryptology ePrint Archive, 2021.

[43] S. Benabbas, R. Gennaro, and Y. Vahlis, "Verifiable delegation of computation over large datasets," in Advances in Cryptology - CRYPTO 2011, pp. 111–131, Springer Berlin Heidelberg, 2011.

[44] Z. Brakerski and V. Vaikuntanathan, "Fully homomorphic encryption from Ring-LWE and security for key dependent messages," in Advances in Cryptology - CRYPTO 2011, pp. 505–524, Springer Berlin Heidelberg, 2011.

[45] A. Nilsson, P. N. Bideh, and J. Brorsson, "A survey of published attacks on intel SGX," June 2020.

[46] S. Fei, Z. Yan, W. Ding, and H. Xie, "Security vulnerabilities of SGX and countermeasures: A survey," ACM Comput. Surv., vol. 54, pp. 1–36, July 2021.

[47] K. Murdock, D. Oswald, F. D. Garcia, J. Van Bulck, D. Gruss, and F. Piessens, "Plundervolt: Software-based fault injection attacks against intel SGX," in 2020 IEEE Symposium on Security and Privacy (SP), pp. 1466–1482, IEEE, May 2020.

[48] A. Wood, K. Najarian, and D. Kahrubaei, "Homomorphic encryption for machine learning in medicine and bioinformatics," ACM Comput. Surv., vol. 53, pp. 1–35, Aug. 2020.

[49] L. B. Pulido-Gaytán, A. Tchernykh, J. M. Cortés-Mendoza, M. Babenko, and G. Radchenko, "A survey on privacy-preserving machine learning with fully homomorphic encryption," in Latin American High Performance Computing Conference, pp. 115–129, Springer, 2021.

[50] C. Marcolla, V. Sucassas, M. Manzano, R. Bassoli, F. H. P. Filtzek, and N. Arau, "Survey on fully homomorphic encryption, theory and applications," Mar. 2022.

[51] K. Kluczniak, "Circuit privacy for FHEW/TFHE-Style fully homomorphic encryption in practice," Cryptology ePrint Archive, 2022.

[52] L. Ducas and D. Stehlé, "Sanitization of FHE ciphersetxts," in Advances in Cryptology - EUROCRYPT 2016, pp. 294–310, Springer Berlin Heidelberg, 2016.

[53] F. Bourse and M. Izabachène, "Plug-and-play sanitization for TFHE," Cryptology ePrint Archive, 2022.

[54] C. Gentry, "Fully homomorphic encryption using ideal lattices," in Proceedings of the forty-first annual ACM symposium on Theory of computing, STOC '09, (New York, NY, USA), pp. 169–178, Association for Computing Machinery, May 2009.

[55] J. H. Cheon, A. Kim, M. Kim, and Y. Song, "Homomorphic encryption for arithmetic of approximate numbers," in Advances in Cryptology - ASIACRYPT 2017, pp. 409–437, Springer International Publishing, 2017.

[56] R. Canetti, S. Raghuraman, S. Richelson, and V. Vaikuntanathan, "Chosen-Ciphertextext secure fully homomorphic encryption," in Public-Key Cryptography - PKC 2017, pp. 213–240, Springer Berlin Heidelberg, 2017.

[57] A. Viand, C. Knabenhans, and A. Hithnawi, "Verifiable fully homomorphic encryption," https://arxiv.org/abs/2301.07041v1, 2023. Extended version (v1).

[58] Z. Brakerski, "Fully homomorphic encryption without modulus switching from classical GapSVP," in Advances in Cryptology CRYPTO 2012, pp. 868–886, Springer Berlin Heidelberg, 2012.

[59] N. P. Smart and F. Vercauteren, "Fully homomorphic SIMD operations," Designs, Codes and Cryptography: An International Journal, vol. 71, pp. 57–81, 1 Apr. 2014.

[60] E. Ben-Sasson, A. Chiesa, D. Genkin, E. Tromer, and M. Virza, "SNARKs for Arithmetic: Verifying program executions succinctly and in zero knowledge," Cryptology ePrint Archive, 2013.

[61] A. Gabizon, Z. J. Aztec, and A. O. Williamson, "PlonK: Permutations over lagrange-bases for decumencal noninteractive arguments of knowledge," https://eprint.iacr.org/2019/953.pdf, 2022. Accessed: 2022-11-2.

[62] B. Chen, B. Bunz, D. Boneh, and Z. Zhang, "HyperPonk: PlonK with Linear-Time prover and High-Degree com gates," Cryptology ePrint Archive, 2022.

[63] E. Ben-Sasson, I. Bentov, Y. Horesh, and M. Riazzev, "Scalable, transparent, and post-quantum secure computational integrity," Cryptology ePrint Archive, 2018.

[64] T. Xie, J. Zhang, Y. Zhang, C. Papamanthou, and D. Song, "Libra: Succinct Zero-Knowledge proofs with optimal prover computation," Cryptology ePrint Archive, 2019.

[65] J. Groth, "On the size of Pairing-Based non-interactive arguments," in Advances in Cryptology - EUROCRYPT 2016, pp. 305–326, Springer Berlin Heidelberg, 2016.

[66] B. Bunz, J. Bootle, D. Borch, A. Poelstra, P. Wuille, and G. Maxwell, "Bulletproofs: Short proofs for confidential transactions and more," in 2018 IEEE Symposium on Security and Privacy (SP), pp. 315–334, May 2018.

[67] E. Ben-Sasson, A. Chiesa, M. Riabzev, N. Spooner, M. Virza, and N. P. Ward, "Aurore: Transparent succinct arguments for RICS," in Advances in Cryptology - EUROCRYPT 2019, pp. 105–128, Springer International Publishing, 2019.

[68] H. García Navarro, "Design and implementation of the circom 1.0 compiler," Master's thesis, Universidad Complutense de Madrid, 2020.

[69] D. arkworks contributors, "arkworks zkSNARK ecosystem," 2022.

[70] D. Cryptography, "Rust Bulletproofs Library," Online: https://github.com/dalek-cryptography/bulletproofs, August 2020.

[71] "Open enclave SDK," https://github.com/openenclave/openenclave.

[72] B. Li, D. Micciancio, M. Schultz, and J. Sorrell, "Securing approximate homomorphic encryption using differential privacy," Cryptology ePrint Archive, 2022.

[73] A. Kim, Y. Polyakov, and V. Zucca, "Revisiting homomorphic encryption schemes for finite fields," Cryptology ePrint Archive, 2021.

[74] F. Boemer, S. Kim, G. Seiffl. F. D. de Souza, V. Gopal, and Others, "Intel HEXL (release 1.2)," https://github.com/intel/hexl, 2021.

[75] O. Ozek, C. Elgezen, A. C. Mert, E. Ozturk, and E. Savas, "Efficient number theoretic transform implementation on GPU for homomorphic encryption," Cryptology ePrint Archive, 2021.

[76] A. Bishnoi, P. L. Clark, A. Pottkuchi, and J. R. Schmitt, "On zeros of a polynomial in a finite grid," Combin. Probab. Comput., vol. 27, pp. 310–333, May 2018.

[77] F. Tramer and D. Boneh, "Shalom: Fast, verifiable and private execution of neural networks in trusted hardware," June 2018.

---



---

[page 17]



---

**Page 18:**

---

**Appendix D.**

In the following, we describe our optimization for FHE-in-TEE: Executing any code inside a TEE incurs a slowdown (due to reduced computational power and memory), especially in the case of FHE computations, that are typically in the case of FHE computations, that are typically compute-and memory-intensive. To alleviate this slowdown, we propose a new method to accelerate FHE computations inside TEEs by taking advantage of faster (but untrusted) hardware (e.g., a vanilla untrusted CPU, a CPU with specialized vector instructions repurposed for FHE [74], a GPU FHE [75], or even a dedicated hardware accelerator).

The key insight to our improvement is that both the TEE and the untrusted hardware are on the side of the (malicious) server. Therefore, the server's input does not need to be protected from the server, and can be stored on the server's own untrusted hardware; the client's inputs are only available in their encrypted form, and can thus also be stored outside the enclave. This insight allows us to devise a protocol for verifiably outsourcing certain FHE operations. In order to do this efficiently, we rely on a very lightweight, information-theoretic argument of equality, based on the generalized Schwartz–Zippel lemma over rings:

**Theorem D.1 (Generalized SZ over Rings [31], [76])**:

For a ring R, let f : Rm → R be a n-variate non-zero polynomial, let A ⊆ R be a finite exceptional set, and let deg(f) denote the total degree of f. Then:

$$
\operatorname{Pr}_{a ← A^{m}} [f(\bar{a}) = 0] \le \frac{\deg(f)}{|A|}
$$

For a given computation, we encode the expected result in one polynomial (f), and the actual result computed on untrusted hardware in another polynomial (g). The trick for efficiency, then, is to compute the compute and compare f(a) and g(a) faster than computing the full representation of g in the first place.

Consider, for example, the tensoring operation, which is the most computationally expensive part of FHE multiplication (for the B/FV, BGV, and CKKS schemes). In the following, we will interpret a ciphertext ct = (ct0, ..., ct_k−1) ∈ Rk as a polynomial of degree k − 1 over Rq, where ct_i is the i-th coefficient.

The tensoring operation takes as input two ciphertexts ct = (ct0, ct1), ct' = (ct'0, ct'1) ∈ Rq^2, and outputs conv = ct · ct' = (ct0 · ct'0, ct0 · ct'1 + ct1 · ct'1) ∈ Rq^2. Now, evaluating the expected result ct · ct' at a random point a ∈ A can be done efficiently as f(a) = (ct0 + a · ct1) · (ct'0 + a · ct'1). Evaluating the untrusted result ct_mat at this same point can be done using Horner's rule: g(a) = ct''(a) = ct'0 + a · ct'1.

After checking that f(a) = g(a), we know that ct·ct' = ct' with high probability (for the FHE schemes discussed in this paper, |A| = q1 ≈ 2^60, i.e., 60 bits of statistical soundness). While computing the result has a concrete complexity of 1 R+R, 4 R^R, verifying the result as outlined above only requires 4 A^R, 4 R+R, 1 R^R.

This approach can also be extended as follows to verify k tensoring operations at the same time. Let f(a1,...,ak) = ∑_{i=1}^k (ct_i · ct'_i)(a_i) = ∑_{i=1}^k (ct_i0 + a_i · ct_i1) · (ct'_i0 + a_i · ct'_i1), and define g(a1,...,ak) = ∑_{i=1}^k (ct'_i0 + a_i · ct'_i1).

Computing k tensoring operations has a concrete complexity of k R+R, 4k R^R, while verifying the result by computing f(a) and g(a) has a complexity of 4k A^R, (6k − 2) R+R, k R^R. By trading expensive R-R multiplications for cheaper R-R additions and A-R multiplications, we are able to achieve a non-negligible speed-up, which we quantify in the next section.

We can view our protocol as a much more efficient, non-zero-knowledge version of Rinocchio; indeed, Rinocchio also uses Theorem D.1, but requires significantly more protocol machinery in order to achieve zero-knowledge. In addition, Rinocchio offers roughly log2 q1 ≈ 60 bits of computational soundness (and thus requires a soundness amplification strategy), while our protocol offers log_q1 bits of statistical soundness, and can therefore provide a satisfactory level of security by itself.

We note that this optimization is similar to the Slalom framework by Tramer and Bonch [77], which offloads matrix multiplications (over unencrypted) values to untrusted hardware by using Freivalds' algorithm. Slalom relies on the TEE both for integrity and data confidentiality and only supports matrix multiplication, whereas our protocol does not require confidentiality of the data stored on the TEE, and can handle arbitrary polynomial computations.