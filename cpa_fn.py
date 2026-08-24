from scipy import stats
import numpy as np
import matplotlib.pyplot as plot

def get_AES_SBox():
     return np.array([
         0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
         0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
         0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
         0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
         0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
         0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
         0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
         0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
         0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
         0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
         0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
         0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
         0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
         0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
         0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
         0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
         ])

def generate_traces_aes(k, l, n_traces, n_feats, noise_gen, t_std = 0,  desync = 0):
    
    # k = correct key
    # l = leakage function (in this exercise, we assume HW)
    # n_traces = no. of traces
    # n_feats = no. of features
    # noise_gen = function to add noise to traces
    # t_std = standard deviation of noises added
    # desync = adjust the shift of features to introduce desynchronization (choose from 0-5)
    
    Sbox = get_AES_SBox()
    
    plaintext = np.random.randint(256,size=n_traces) # generate 'n_traces' plaintexts (1-byte)
    
    sbox_iv = np.zeros(n_traces)
    for i in range(n_traces):
       sbox_iv[i] = Sbox[k^int(plaintext[i])] # calculate the actual intermediate value
    
    sbox_hw = np.zeros(n_traces)
    for i in range(n_traces):
       sbox_hw[i] = l(sbox_iv[i]) # calculate the leakage based on leakage function 'l' (in this case HW)
       
    trace = np.zeros((n_traces,n_feats))
    # Insert the simulated leakage at a random point of interest (POI)
    poi = np.random.randint(n_feats)
    trace[:,poi] = sbox_hw
    trace = noise_gen(trace,t_std)
    
    if desync > 0:
        trace_desync = np.zeros((n_traces,n_feats))
        for i in range(n_traces):
            idx = np.random.randint(desync+1) 
            temp =  trace[i,idx:idx+trace_desync.shape[1]]
            trace_desync[i,:len(temp)] = temp
        trace = trace_desync
    
    return plaintext, trace
    
def perform_cpa_aes(pt, t, L, c):
    
    # pt = plaintexts array
    # t = side-channel traces
    # L = leakage model (approximation of leakage function l), for simulation, we use HW
    # c = the function to calculate correlation

    Sbox = get_AES_SBox()
    n_traces = t.shape[0]
    key_cand = 256
    
    hyp_model = np.zeros((key_cand, n_traces))
    for k in range(256):
        for i in range(n_traces):
            hyp_model[k,i] = L(Sbox[k^int(pt[i])])
            
    corr_array = np.zeros((key_cand,t.shape[1]))

    for k in range(256):
        corr_array[k,:] = c(hyp_model[k,:], t)
    
    return corr_array
    
def plot_traces(t):
    
    n = min(10,t.shape[0])
    for i in range(n):
        plot.plot(t[i,:], alpha=0.7)
    plot.xlabel("Time Sample")
    plot.ylabel("Amplitude")
    plot.title("Traces")
    
def plot_cpa_all_points(corr_array, ck):
    
    # only when number of features > 1:
    # corr_array = returned correlation matrix from CPA
    # ck = correct key
    
    plot.figure()
    for k in range(256):
        if k == ck:
            plot.plot(corr_array[k,:],'k', linewidth=2)
        else:
            plot.plot(corr_array[k,:],'r', alpha=0.15)
    plot.xlabel("Time Sample")
    plot.ylabel("|Correlation|")
    plot.ylim(0,1)
    plot.title("CPA on simulated traces (Black = correct key)")
    plot.show()
    
def plot_cpa_key_comp(corr_array, ck):
    
    # corr_array = returned correlation matrix from CPA
    # ck = correct key
    
    correlation_values_max = np.zeros(256)
    for i in range(256):
        correlation_values_max[i] = max(corr_array[i,:])
    
    plot.figure()
    x_index = np.arange(256)
    plot.plot(x_index,correlation_values_max)
    plot.plot(ck, correlation_values_max[ck],'r*')
    plot.xlabel("Key Candidate")
    plot.ylabel("|Correlation|")
    plot.ylim(0,1)
    plot.title("Multiple feats: CPA on simulated traces (* is correct key)")
    plot.show()

def print_cpa_aes(corr_array, ck):

    # corr_array = correlation matrix returned by CPA
    # ck = correct key

    correlation_values_max = np.zeros(256)

    for i in range(256):
        correlation_values_max[i] = np.max(np.abs(corr_array[i, :]))

    sorting_order = np.argsort(correlation_values_max)[::-1]

    rank_of_correct_key = np.where(sorting_order == ck)[0][0]
    best_key = sorting_order[0]

    print("\nCPA Results:")
    print("Best Key Candidate: 0x{:02X}".format(best_key))
    print("Correct Key:       0x{:02X}".format(ck))
    print("Rank of Correct Key: {}".format(rank_of_correct_key + 1))
    print("Maximum Correlation: {:.4f}".format(
        correlation_values_max[best_key]
    ))