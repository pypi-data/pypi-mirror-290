#ifndef CASM_clexmonte_system_data
#define CASM_clexmonte_system_data

#include <set>
#include <string>
#include <vector>

#include "casm/clexulator/SparseCoefficients.hh"
#include "casm/configuration/clusterography/IntegralCluster.hh"
#include "casm/configuration/occ_events/OccEvent.hh"
#include "casm/crystallography/SymType.hh"
#include "casm/crystallography/UnitCellCoord.hh"
#include "casm/global/definitions.hh"

namespace CASM {

namespace config {
struct Prim;
}

namespace occ_events {
struct OccEventRep;
}

namespace clexmonte {

struct BasisSetClusterInfo {
  /// Cluster orbits, in order matching a Clexulator
  std::vector<std::set<clust::IntegralCluster>> orbits;

  /// Convert linear function index to linear cluster orbit index
  std::vector<Index> function_to_orbit_index;
};

/// \brief Expand a required_update_neighborhood based on
///     BasisSetClusterInfo and SparseCoefficients
void expand(clust::IntegralCluster const &phenom,
            std::set<xtal::UnitCellCoord> &required_update_neighborhood,
            BasisSetClusterInfo const &cluster_info,
            clexulator::SparseCoefficients const &coefficients);

struct ClexData {
  std::string basis_set_name;
  clexulator::SparseCoefficients coefficients;
  std::shared_ptr<BasisSetClusterInfo const> cluster_info;
};

struct MultiClexData {
  std::string basis_set_name;
  std::vector<clexulator::SparseCoefficients> coefficients;
  std::shared_ptr<BasisSetClusterInfo const> cluster_info;

  /// \brief Map of key ("kra", "freq", etc.) to coefficients index
  std::map<std::string, Index> coefficients_glossary;
};

/// \brief Info on local cluster expansion basis sets
///
/// Note:
/// - This is meant to be constructed from the information stored in
///   an "equivalents_info.json" file when CASM generates a local
///   Clexulator. It specifies the phenomenal clusters for each local
///   basis set, and the prim factor group operations that can be used
///   to construct the equivalent local basis sets from the first.
///   Proper operation requires that the same prim factor group, in the
///   same order, is used to generate the local basis set and to
///   construct this.
///
/// TODO: This should in CASMcode_clexulator,
/// using std::vector<xtal::UnitCellCoord> for cluster
struct EquivalentsInfo {
  EquivalentsInfo(
      config::Prim const &_prim,
      std::vector<clust::IntegralCluster> const &_phenomenal_clusters,
      std::vector<Index> const &_equivalent_generating_op_indices);

  /// \brief Phenomenal clusters for each equivalent local basis set
  std::vector<clust::IntegralCluster> phenomenal_clusters;

  /// \brief Indices of prim factor group operations that generate
  ///     the equivalent local basis sets from the first
  std::vector<Index> equivalent_generating_op_indices;

  /// \brief xtal::Symop operations that generate
  ///     the equivalent phenomenal clusters from the first, including
  ///     the proper translation
  std::vector<xtal::SymOp> equivalent_generating_ops;

  /// \brief The proper translations (applied after factor group op)
  std::vector<xtal::UnitCell> translations;
};

/// \brief Make equivalents by applying symmetry,
///     such that `equivalents[i] == copy_apply(occevent_symgroup_rep[i], event)
///     + info.translations[i]`
std::vector<occ_events::OccEvent> make_equivalents(
    occ_events::OccEvent const &event, EquivalentsInfo const &info,
    std::vector<occ_events::OccEventRep> const &occevent_symgroup_rep);

bool is_same_phenomenal_clusters(
    std::vector<occ_events::OccEvent> const &equivalents,
    EquivalentsInfo const &info);

struct LocalClexData {
  std::string local_basis_set_name;
  clexulator::SparseCoefficients coefficients;
};

struct LocalMultiClexData {
  std::string local_basis_set_name;
  std::vector<clexulator::SparseCoefficients> coefficients;

  /// \brief Map of key ("kra", "freq", etc.) to coefficients index
  std::map<std::string, Index> coefficients_glossary;
};

/// \brief KMC event data
///
/// Note:
/// - These events should agree in translation and orientation with
///   the local cluster expansion basis set(s) used to calculate
///   properties. To ensure this, the first event should have the
///   same phenomenal cluster as the first local basis set, and
///   EquivalentsInfo::equivalent_generating_ops should be used
///   to construct the equivalent events.
struct OccEventTypeData {
  /// \brief Vector of symmetrically equivalent events
  ///
  /// For consistency between local basis set and the equivalent events,
  /// this should be generated with:
  /// \code
  /// make_equivalents(
  ///     occ_events::OccEvent const &event,
  ///     EquivalentsInfo const &info,
  ///     std::vector<occ_events::OccEventRep> const &occevent_symgroup_rep);
  /// \endcode
  /// where `event` shares the phenomenal cluster used to generate the
  /// local basis set, `info` is read from an `equivalents_info.json`
  /// file generated when the local basis set is generated, and
  /// `occevent_symgroup_rep` is a representation of the prim factor group.
  std::vector<occ_events::OccEvent> events;

  /// \brief The name of the local_multiclex used for event properties, if
  /// applicable
  std::string local_multiclex_name;
};

}  // namespace clexmonte
}  // namespace CASM

#endif
