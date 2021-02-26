struct imm_abc;
struct imm_abc_lprob;
struct imm_dp;
struct imm_dp_task;
struct imm_hmm;
struct imm_input;
struct imm_model;
struct imm_mute_state;
struct imm_normal_state;
struct imm_output;
struct imm_path;
struct imm_profile;
struct imm_result;
struct imm_seq;
struct imm_seq_table;
struct imm_state;
struct imm_step;
struct imm_table_state;

typedef __IMM_FLOAT__ imm_float;

#define IMM_MUTE_STATE_TYPE_ID 0x00
#define IMM_NORMAL_STATE_TYPE_ID 0x01
#define IMM_TABLE_STATE_TYPE_ID 0x02

enum imm_symbol_type
{
    IMM_SYMBOL_UNKNOWN = 0,
    IMM_SYMBOL_NORMAL = 1,
    IMM_SYMBOL_ANY = 2,
};

/**
 * Sequence of characters. No need for null-terminated string.
 */
struct imm_seq
{
    struct imm_abc const* abc;
    char const*           string;
    uint32_t              length;
};

/* Alphabet */
char                  imm_abc_any_symbol(struct imm_abc const* abc);
struct imm_abc const* imm_abc_clone(struct imm_abc const* abc);
struct imm_abc const* imm_abc_create(char const* symbols, char any_symbol);
void                  imm_abc_destroy(struct imm_abc const* abc);
bool                  imm_abc_has_symbol(struct imm_abc const* abc, char symbol_id);
uint8_t               imm_abc_length(struct imm_abc const* abc);
struct imm_abc*       imm_abc_read(FILE* stream);
char                  imm_abc_symbol_id(struct imm_abc const* abc, uint8_t symbol_idx);
uint8_t               imm_abc_symbol_idx(struct imm_abc const* abc, char symbol_id);
enum imm_symbol_type  imm_abc_symbol_type(struct imm_abc const* abc, char symbol_id);
char const*           imm_abc_symbols(struct imm_abc const* abc);
uint8_t               imm_abc_type_id(struct imm_abc const* abc);
int                   imm_abc_write(struct imm_abc const* abc, FILE* stream);

/* Alphabet lprob */
struct imm_abc_lprob const* imm_abc_lprob_create(struct imm_abc const* abc, imm_float const* lprobs);
void                        imm_abc_lprob_destroy(struct imm_abc_lprob const* abc_lprob);
struct imm_abc const*       imm_abc_lprob_abc(struct imm_abc_lprob const* abc_lprob);
imm_float                   imm_abc_lprob_get(struct imm_abc_lprob const* abc_lprob, char symbol);

/* DP */
void                     imm_dp_destroy(struct imm_dp const* dp);
struct imm_result const* imm_dp_viterbi(struct imm_dp const* dp, struct imm_dp_task* task);
int                      imm_dp_change_trans(struct imm_dp* dp, struct imm_hmm* hmm, struct imm_state const* src_state,
                                             struct imm_state const* tgt_state, imm_float lprob);
/* DP task */
struct imm_dp_task* imm_dp_task_create(struct imm_dp const* dp);
void                imm_dp_task_setup(struct imm_dp_task* task, struct imm_seq const* seq);
void                imm_dp_task_destroy(struct imm_dp_task const* dp_task);

/* HMM */
int             imm_hmm_add_state(struct imm_hmm* hmm, struct imm_state const* state, imm_float start_lprob);
struct imm_hmm* imm_hmm_create(struct imm_abc const* abc);
struct imm_dp*  imm_hmm_create_dp(struct imm_hmm const* hmm, struct imm_state const* end_state);
int             imm_hmm_del_state(struct imm_hmm* hmm, struct imm_state const* state);
void            imm_hmm_destroy(struct imm_hmm const* hmm);
imm_float       imm_hmm_get_trans(struct imm_hmm const* hmm, struct imm_state const* src_state,
                                  struct imm_state const* tgt_state);
imm_float imm_hmm_loglikelihood(struct imm_hmm const* hmm, struct imm_seq const* seq, struct imm_path const* path);
int       imm_hmm_normalize(struct imm_hmm* hmm);
int       imm_hmm_normalize_start(struct imm_hmm* hmm);
int       imm_hmm_normalize_trans(struct imm_hmm* hmm, struct imm_state const* src_state);
imm_float imm_hmm_get_start(struct imm_hmm const* hmm, struct imm_state const* state);
int       imm_hmm_set_start(struct imm_hmm* hmm, struct imm_state const* state, imm_float lprob);
int       imm_hmm_set_trans(struct imm_hmm* hmm, struct imm_state const* src_state, struct imm_state const* tgt_state,
                            imm_float lprob);

/* Model */
struct imm_model*       imm_model_create(struct imm_hmm* hmm, struct imm_dp const* dp);
void                    imm_model_destroy(struct imm_model const* model, bool deep);
struct imm_dp const*    imm_model_dp(struct imm_model const* model);
struct imm_hmm*         imm_model_hmm(struct imm_model const* model);
uint16_t                imm_model_nstates(struct imm_model const* model);
struct imm_state const* imm_model_state(struct imm_model const* model, uint16_t i);

/* Input */
int                       imm_input_close(struct imm_input* input);
struct imm_input*         imm_input_create(char const* filepath);
int                       imm_input_destroy(struct imm_input* input);
bool                      imm_input_eof(struct imm_input const* input);
struct imm_profile const* imm_input_read(struct imm_input* input);

/* Profile */
struct imm_abc const*     imm_profile_abc(struct imm_profile const* prof);
void                      imm_profile_append_model(struct imm_profile* prof, struct imm_model* model);
struct imm_profile*       imm_profile_create(struct imm_abc const* abc);
void                      imm_profile_destroy(struct imm_profile const* prof, bool deep);
void                      imm_profile_free(struct imm_profile const* prof);
struct imm_model*         imm_profile_get_model(struct imm_profile const* prof, uint8_t i);
uint8_t                   imm_profile_nmodels(struct imm_profile const* prof);
struct imm_profile const* imm_profile_read(FILE* stream);
int                       imm_profile_write(struct imm_profile const* prof, FILE* stream);

/* Mute state */
struct imm_mute_state const* imm_mute_state_create(char const* name, struct imm_abc const* abc);
struct imm_mute_state const* imm_mute_state_derived(struct imm_state const* state);
void                         imm_mute_state_destroy(struct imm_mute_state const* state);
struct imm_state const*      imm_mute_state_read(FILE* stream, struct imm_abc const* abc);
struct imm_state const*      imm_mute_state_super(struct imm_mute_state const* state);
int imm_mute_state_write(struct imm_state const* state, struct imm_profile const* prof, FILE* stream);

/* Normal state */
struct imm_normal_state const* imm_normal_state_create(char const* name, struct imm_abc const* abc,
                                                       imm_float const* lprobs);
struct imm_normal_state const* imm_normal_state_derived(struct imm_state const* state);
void                           imm_normal_state_destroy(struct imm_normal_state const* state);
struct imm_state const*        imm_normal_state_read(FILE* stream, struct imm_abc const* abc);
struct imm_state const*        imm_normal_state_super(struct imm_normal_state const* state);
int imm_normal_state_write(struct imm_state const* state, struct imm_profile const* prof, FILE* stream);

/* Output */
int                imm_output_close(struct imm_output* output);
struct imm_output* imm_output_create(char const* filepath);
int                imm_output_destroy(struct imm_output* output);
int                imm_output_write(struct imm_output* output, struct imm_profile const* prof);

/* Path */
void                   imm_path_append(struct imm_path* path, struct imm_step* step);
struct imm_path*       imm_path_clone(struct imm_path const* path);
struct imm_path*       imm_path_create(void);
void                   imm_path_destroy(struct imm_path const* path);
struct imm_step const* imm_path_first(struct imm_path const* path);
void                   imm_path_free(struct imm_path const* path);
struct imm_step const* imm_path_next(struct imm_path const* path, struct imm_step const* step);
void                   imm_path_prepend(struct imm_path* path, struct imm_step* step);

/* Result */
struct imm_result*     imm_result_create(struct imm_seq const* seq);
void                   imm_result_destroy(struct imm_result const* result);
void                   imm_result_free(struct imm_result const* result);
struct imm_path const* imm_result_path(struct imm_result const* result);
imm_float              imm_result_seconds(struct imm_result const* result);

/* Sequence */
struct imm_seq const* imm_seq_clone(struct imm_seq const* seq);
struct imm_seq const* imm_seq_create(char const* string, struct imm_abc const* abc);
void                  imm_seq_destroy(struct imm_seq const* seq);
struct imm_abc const* imm_seq_get_abc(struct imm_seq const* seq);
uint32_t              imm_seq_length(struct imm_seq const* seq);
char const*           imm_seq_string(struct imm_seq const* seq);

/* Sequence table */
struct imm_abc const* imm_seq_table_abc(struct imm_seq_table const* table);
int                   imm_seq_table_add(struct imm_seq_table* table, struct imm_seq const* seq, imm_float lprob);
struct imm_seq_table* imm_seq_table_clone(struct imm_seq_table const* table);
struct imm_seq_table* imm_seq_table_create(struct imm_abc const* abc);
void                  imm_seq_table_destroy(struct imm_seq_table const* table);
imm_float             imm_seq_table_lprob(struct imm_seq_table const* table, struct imm_seq const* seq);
uint8_t               imm_seq_table_max_seq(struct imm_seq_table const* table);
uint8_t               imm_seq_table_min_seq(struct imm_seq_table const* table);
int                   imm_seq_table_normalize(struct imm_seq_table* table);

/* State */
struct imm_state const* imm_state_create(char const* name, struct imm_abc const* abc, struct imm_state_vtable vtable,
                                         void* derived);
void                    imm_state_destroy(struct imm_state const* state);
struct imm_abc const*   imm_state_get_abc(struct imm_state const* state);
char const*             imm_state_get_name(struct imm_state const* state);
imm_float               imm_state_lprob(struct imm_state const* state, struct imm_seq const* seq);
uint8_t                 imm_state_max_seq(struct imm_state const* state);
uint8_t                 imm_state_min_seq(struct imm_state const* state);
uint8_t                 imm_state_type_id(struct imm_state const* state);

/* Step */
struct imm_step*        imm_step_clone(struct imm_step const* step);
struct imm_step*        imm_step_create(struct imm_state const* state, uint8_t seq_len);
void                    imm_step_destroy(struct imm_step const* step);
uint8_t                 imm_step_seq_len(struct imm_step const* step);
struct imm_state const* imm_step_state(struct imm_step const* step);

/* Subseq */
static inline void imm_subseq_set(struct imm_seq* subseq, struct imm_seq const* seq, uint32_t start, uint32_t length);

/* Table state */
struct imm_table_state const* imm_table_state_create(char const* name, struct imm_seq_table const* table);
struct imm_table_state const* imm_table_state_derived(struct imm_state const* state);
void                          imm_table_state_destroy(struct imm_table_state const* state);
struct imm_state const*       imm_table_state_read(FILE* stream, struct imm_abc const* abc);
struct imm_state const*       imm_table_state_super(struct imm_table_state const* state);
int imm_table_state_write(struct imm_state const* state, struct imm_profile const* prof, FILE* stream);

/* Probabilities */
imm_float imm_lprob_add(imm_float a, imm_float b);
imm_float imm_lprob_invalid(void);
bool      imm_lprob_is_valid(imm_float a);
bool      imm_lprob_is_zero(imm_float a);
int       imm_lprob_normalize(imm_float* arr, size_t len);
imm_float imm_lprob_sum(imm_float const* arr, size_t len);
imm_float imm_lprob_zero(void);
