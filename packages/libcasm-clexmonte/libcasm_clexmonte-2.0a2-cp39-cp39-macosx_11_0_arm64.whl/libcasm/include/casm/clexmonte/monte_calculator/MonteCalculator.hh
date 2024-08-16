#ifndef CASM_clexmonte_MonteCalculator
#define CASM_clexmonte_MonteCalculator

#include "casm/clexmonte/monte_calculator/BaseMonteCalculator.hh"

namespace CASM {
namespace clexmonte {

/// \brief Implements a potential
class MontePotential {
 public:
  MontePotential(std::shared_ptr<BaseMontePotential> _pot,
                 std::shared_ptr<RuntimeLibrary> _lib)
      : m_pot(_pot), m_lib(_lib) {}

  ~MontePotential() {
    // ensure BaseMontePotential is deleted before library
    m_pot.reset();
  }

  /// State data for sampling functions, for the current state
  std::shared_ptr<StateData> state_data() { return m_pot->state_data; }

  /// \brief Calculate (per_supercell) potential value
  double per_supercell() { return m_pot->per_supercell(); }

  /// \brief Calculate (per_unitcell) potential value
  double per_unitcell() { return m_pot->per_unitcell(); }

  /// \brief Calculate change in (per_supercell) semi-grand potential value due
  ///     to a series of occupation changes
  double occ_delta_per_supercell(std::vector<Index> const &linear_site_index,
                                 std::vector<int> const &new_occ) {
    return m_pot->occ_delta_per_supercell(linear_site_index, new_occ);
  }

 private:
  std::shared_ptr<BaseMontePotential> m_pot;
  std::shared_ptr<RuntimeLibrary> m_lib;
};

/// \brief Wrapper for Monte Carlo calculations implementations
class MonteCalculator {
 public:
  typedef std::mt19937_64 engine_type;
  typedef monte::KMCData<config_type, statistics_type, engine_type>
      kmc_data_type;

  /// \brief Constructor.
  ///
  /// Note: For most uses it is recommended to construct
  /// a std::shared_ptr<MonteCalculator> using the `make_monte_calculator`
  /// factory function.
  ///
  /// \param _base_calculator The underlying implementation
  /// \param _lib If the `base_calculator` is from a runtime library, it should
  ///     be provided to ensure the lifetime of the library. Otherwise, give
  ///     nullptr.
  MonteCalculator(
      std::unique_ptr<clexmonte::BaseMonteCalculator> _base_calculator,
      std::shared_ptr<RuntimeLibrary> _lib)
      : m_calc(_base_calculator), m_lib(_lib) {}

  ~MonteCalculator() {
    // ensure BaseMonteCalculator is deleted before library
    m_calc.reset();
  }

  // --- Set at construction: ---

  /// Calculator name
  std::string const &calculator_name() const { return m_calc->calculator_name; }

  /// Method allows time-based sampling?
  bool time_sampling_allowed() const { return m_calc->time_sampling_allowed; }

  /// Method tracks species locations? (like in KMC)
  bool update_species() const { return m_calc->update_species; }

  // --- Set at `reset`: ---

  /// \brief Set parameters, check for required system data, and reset derived
  /// Monte Carlo calculator
  void reset(jsonParser const &_params, std::shared_ptr<system_type> system) {
    m_calc->reset(_params, system);
  }

  /// Calculator method parameters
  jsonParser const &params() const { return m_calc->params; }

  /// System data
  std::shared_ptr<system_type> system() const { return m_calc->system; }

  // --- Set by user after `reset`, before `run`: ---

  /// State sampling functions
  std::map<std::string, state_sampling_function_type> sampling_functions;

  /// JSON State sampling functions
  std::map<std::string, json_state_sampling_function_type>
      json_sampling_functions;

  /// Results analysis functions
  std::map<std::string, results_analysis_function_type> analysis_functions;

  /// State modifying functions
  StateModifyingFunctionMap modifying_functions;

  // --- Set when `set_state_and_potential` or `run` is called: ---

  /// State data for sampling functions, for the current state
  std::shared_ptr<StateData> state_data() {
    if (m_calc->state_data == nullptr) {
      throw std::runtime_error(
          "Error in MonteCalculator::state_data: State data is not "
          "yet constructed. To use outside of the `run` method, call "
          "`set_state_and_potential` first.");
    }
    return m_calc->state_data;
  }

  /// \brief Potential calculator
  MontePotential potential() {
    if (m_calc->potential == nullptr) {
      throw std::runtime_error(
          "Error in MonteCalculator::potential: Potential calculator is not "
          "yet constructed. To use outside of the `run` method, call "
          "`set_state_and_potential` first.");
    }
    return MontePotential(m_calc->potential, m_lib);
  }

  /// \brief Validate the state's configuration
  Validator validate_configuration(state_type &state) const {
    return m_calc->validate_configuration(state);
  }

  /// \brief Validate the state's conditions
  Validator validate_conditions(state_type &state) const {
    return m_calc->validate_conditions(state);
  }

  /// \brief Validate the state
  Validator validate_state(state_type &state) const {
    return m_calc->validate_state(state);
  }

  /// \brief Validate and set the current state, construct state_data, construct
  ///     potential
  void set_state_and_potential(state_type &state,
                               monte::OccLocation *occ_location) {
    return m_calc->set_state_and_potential(state, occ_location);
  }

  // --- Set when `run` is called: ---

  /// KMC data for sampling functions, for the current state (if applicable)
  std::shared_ptr<kmc_data_type> kmc_data() {
    if (m_calc->kmc_data == nullptr) {
      throw std::runtime_error(
          "Error in MonteCalculator::kmc_data: KMC data is not "
          "yet constructed.");
    }
    return m_calc->kmc_data;
  }

  /// \brief Perform a single run, evolving current state
  void run(state_type &state, monte::OccLocation &occ_location,
           run_manager_type<engine_type> &run_manager) {
    m_calc->run(state, occ_location, run_manager);
  }

  /// \brief Construct functions that may be used to sample various quantities
  /// of
  ///     the Monte Carlo calculation as it runs
  std::map<std::string, state_sampling_function_type>
  standard_sampling_functions(
      std::shared_ptr<MonteCalculator> const &calculation) const {
    return m_calc->standard_sampling_functions(calculation);
  }

  /// \brief Construct functions that may be used to sample various quantities
  ///     of the Monte Carlo calculation as it runs
  std::map<std::string, json_state_sampling_function_type>
  standard_json_sampling_functions(
      std::shared_ptr<MonteCalculator> const &calculation) const {
    return m_calc->standard_json_sampling_functions(calculation);
  }

  /// \brief Construct functions that may be used to analyze Monte Carlo
  ///     calculation results
  std::map<std::string, results_analysis_function_type>
  standard_analysis_functions(
      std::shared_ptr<MonteCalculator> const &calculation) const {
    return m_calc->standard_analysis_functions(calculation);
  }

  /// \brief Construct functions that may be used to modify states
  StateModifyingFunctionMap standard_modifying_functions(
      std::shared_ptr<MonteCalculator> const &calculation) const {
    return m_calc->standard_modifying_functions(calculation);
  }

  /// \brief Construct default SamplingFixtureParams
  sampling_fixture_params_type make_default_sampling_fixture_params(
      std::shared_ptr<MonteCalculator> const &calculation, std::string label,
      bool write_results = true, bool write_trajectory = false,
      bool write_observations = false, bool write_status = true,
      std::optional<std::string> output_dir = std::nullopt,
      std::optional<std::string> log_file = std::nullopt,
      double log_frequency_in_s = 600.0) const {
    return m_calc->make_default_sampling_fixture_params(
        calculation, label, write_results, write_trajectory, write_observations,
        write_status, output_dir, log_file, log_frequency_in_s);
  }

  // --- Experimental, to support multi-state methods: ---

  /// \brief Check if a multi-state method
  bool is_multistate_method() const { return m_calc->is_multistate_method; }

  /// \brief Number of states, for multi-state methods
  int n_states() const { return m_calc->multistate_data.size(); }

  /// \brief Current state index
  int current_state() const { return m_calc->current_state; }

  /// \brief State data for sampling functions, for specified state
  std::shared_ptr<StateData> multistate_state_data(int state_index) {
    return m_calc->multistate_data.at(state_index);
  }

  /// \brief Potential calculator, for specified state
  MontePotential multistate_potential(int state_index) {
    return MontePotential(m_calc->multistate_potential.at(state_index), m_lib);
  }

  /// \brief Perform a single run, evolving one or more states
  void run(int current_state, std::vector<state_type> &states,
           std::vector<monte::OccLocation> &occ_locations,
           run_manager_type<engine_type> &run_manager) {
    m_calc->run(current_state, states, occ_locations, run_manager);
  }

 private:
  notstd::cloneable_ptr<BaseMonteCalculator> m_calc;
  std::shared_ptr<RuntimeLibrary> m_lib;
};

/// \brief MonteCalculator factory function
std::shared_ptr<MonteCalculator> make_monte_calculator(
    jsonParser const &params, std::shared_ptr<system_type> system,
    std::unique_ptr<BaseMonteCalculator> base_calculator,
    std::shared_ptr<RuntimeLibrary> lib);

/// \brief MonteCalculator factory function, from source
std::shared_ptr<MonteCalculator> make_monte_calculator_from_source(
    fs::path dirpath, std::string calculator_name, jsonParser const &params,
    std::shared_ptr<system_type> system, std::string compile_options,
    std::string so_options);

Eigen::VectorXd scalar_conditions(
    std::shared_ptr<MonteCalculator> const &calculation, std::string key);

Eigen::VectorXd vector_conditions(
    std::shared_ptr<MonteCalculator> const &calculation, std::string key);

Eigen::VectorXd matrix_conditions(
    std::shared_ptr<MonteCalculator> const &calculation, std::string key);

system_type const &get_system(
    std::shared_ptr<MonteCalculator> const &calculation);

state_type const &get_state(
    std::shared_ptr<MonteCalculator> const &calculation);

/// \brief Make temporary monte::OccLocation if necessary
void make_temporary_if_necessary(state_type const &state,
                                 monte::OccLocation *&occ_location,
                                 std::unique_ptr<monte::OccLocation> &tmp,
                                 MonteCalculator const &calculation);

}  // namespace clexmonte
}  // namespace CASM

#endif
