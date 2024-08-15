#include <Pythia8/Analysis.h>
#include <Pythia8/Basics.h>
#include <Pythia8/Event.h>
#include <Pythia8/Info.h>
#include <Pythia8/ParticleData.h>
#include <Pythia8/ResonanceWidths.h>
#include <istream>
#include <iterator>
#include <memory>
#include <ostream>
#include <sstream> // __str__
#include <string>
#include <utility>
#include <vector>

#include <pybind11/pybind11.h>
#include <functional>
#include <string>
#include <Pythia8/UserHooks.h>
#include <Pythia8/HeavyIons.h>
#include <Pythia8/BeamShape.h>
#include <pybind11/stl.h>
#include <pybind11/complex.h>
#include <pybind11/functional.h>


#ifndef BINDER_PYBIND11_TYPE_CASTER
	#define BINDER_PYBIND11_TYPE_CASTER
	PYBIND11_DECLARE_HOLDER_TYPE(T, std::shared_ptr<T>);
	PYBIND11_DECLARE_HOLDER_TYPE(T, T*);
	PYBIND11_MAKE_OPAQUE(std::shared_ptr<void>);
#endif

// Pythia8::SlowJetHook file:Pythia8/Analysis.h line:371
struct PyCallBack_Pythia8_SlowJetHook : public Pythia8::SlowJetHook {
	using Pythia8::SlowJetHook::SlowJetHook;

	bool include(int a0, const class Pythia8::Event & a1, class Pythia8::Vec4 & a2, double & a3) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SlowJetHook *>(this), "include");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"SlowJetHook::include\"");
	}
};

// Pythia8::SlowJet file:Pythia8/Analysis.h line:422
struct PyCallBack_Pythia8_SlowJet : public Pythia8::SlowJet {
	using Pythia8::SlowJet::SlowJet;

	bool doStep() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SlowJet *>(this), "doStep");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return SlowJet::doStep();
	}
	void findNext() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::SlowJet *>(this), "findNext");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return SlowJet::findNext();
	}
};

void bind_Pythia8_Analysis(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // Pythia8::Sphericity file:Pythia8/Analysis.h line:27
		pybind11::class_<Pythia8::Sphericity, std::shared_ptr<Pythia8::Sphericity>> cl(M("Pythia8"), "Sphericity", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::Sphericity(); } ), "doc" );
		cl.def( pybind11::init( [](double const & a0){ return new Pythia8::Sphericity(a0); } ), "doc" , pybind11::arg("powerIn"));
		cl.def( pybind11::init<double, int>(), pybind11::arg("powerIn"), pybind11::arg("selectIn") );

		cl.def("analyze", (bool (Pythia8::Sphericity::*)(const class Pythia8::Event &)) &Pythia8::Sphericity::analyze, "C++: Pythia8::Sphericity::analyze(const class Pythia8::Event &) --> bool", pybind11::arg("event"));
		cl.def("sphericity", (double (Pythia8::Sphericity::*)() const) &Pythia8::Sphericity::sphericity, "C++: Pythia8::Sphericity::sphericity() const --> double");
		cl.def("aplanarity", (double (Pythia8::Sphericity::*)() const) &Pythia8::Sphericity::aplanarity, "C++: Pythia8::Sphericity::aplanarity() const --> double");
		cl.def("eigenValue", (double (Pythia8::Sphericity::*)(int) const) &Pythia8::Sphericity::eigenValue, "C++: Pythia8::Sphericity::eigenValue(int) const --> double", pybind11::arg("i"));
		cl.def("eventAxis", (class Pythia8::Vec4 (Pythia8::Sphericity::*)(int) const) &Pythia8::Sphericity::eventAxis, "C++: Pythia8::Sphericity::eventAxis(int) const --> class Pythia8::Vec4", pybind11::arg("i"));
		cl.def("list", (void (Pythia8::Sphericity::*)() const) &Pythia8::Sphericity::list, "C++: Pythia8::Sphericity::list() const --> void");
		cl.def("nError", (int (Pythia8::Sphericity::*)() const) &Pythia8::Sphericity::nError, "C++: Pythia8::Sphericity::nError() const --> int");
	}
	{ // Pythia8::Thrust file:Pythia8/Analysis.h line:80
		pybind11::class_<Pythia8::Thrust, std::shared_ptr<Pythia8::Thrust>> cl(M("Pythia8"), "Thrust", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::Thrust(); } ), "doc" );
		cl.def( pybind11::init<int>(), pybind11::arg("selectIn") );

		cl.def("analyze", (bool (Pythia8::Thrust::*)(const class Pythia8::Event &)) &Pythia8::Thrust::analyze, "C++: Pythia8::Thrust::analyze(const class Pythia8::Event &) --> bool", pybind11::arg("event"));
		cl.def("thrust", (double (Pythia8::Thrust::*)() const) &Pythia8::Thrust::thrust, "C++: Pythia8::Thrust::thrust() const --> double");
		cl.def("tMajor", (double (Pythia8::Thrust::*)() const) &Pythia8::Thrust::tMajor, "C++: Pythia8::Thrust::tMajor() const --> double");
		cl.def("tMinor", (double (Pythia8::Thrust::*)() const) &Pythia8::Thrust::tMinor, "C++: Pythia8::Thrust::tMinor() const --> double");
		cl.def("oblateness", (double (Pythia8::Thrust::*)() const) &Pythia8::Thrust::oblateness, "C++: Pythia8::Thrust::oblateness() const --> double");
		cl.def("eventAxis", (class Pythia8::Vec4 (Pythia8::Thrust::*)(int) const) &Pythia8::Thrust::eventAxis, "C++: Pythia8::Thrust::eventAxis(int) const --> class Pythia8::Vec4", pybind11::arg("i"));
		cl.def("list", (void (Pythia8::Thrust::*)() const) &Pythia8::Thrust::list, "C++: Pythia8::Thrust::list() const --> void");
		cl.def("nError", (int (Pythia8::Thrust::*)() const) &Pythia8::Thrust::nError, "C++: Pythia8::Thrust::nError() const --> int");
	}
	{ // Pythia8::ClusterJet file:Pythia8/Analysis.h line:179
		pybind11::class_<Pythia8::ClusterJet, std::shared_ptr<Pythia8::ClusterJet>> cl(M("Pythia8"), "ClusterJet", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::ClusterJet(); } ), "doc" );
		cl.def( pybind11::init( [](class std::basic_string<char> const & a0){ return new Pythia8::ClusterJet(a0); } ), "doc" , pybind11::arg("measureIn"));
		cl.def( pybind11::init( [](class std::basic_string<char> const & a0, int const & a1){ return new Pythia8::ClusterJet(a0, a1); } ), "doc" , pybind11::arg("measureIn"), pybind11::arg("selectIn"));
		cl.def( pybind11::init( [](class std::basic_string<char> const & a0, int const & a1, int const & a2){ return new Pythia8::ClusterJet(a0, a1, a2); } ), "doc" , pybind11::arg("measureIn"), pybind11::arg("selectIn"), pybind11::arg("massSetIn"));
		cl.def( pybind11::init( [](class std::basic_string<char> const & a0, int const & a1, int const & a2, bool const & a3){ return new Pythia8::ClusterJet(a0, a1, a2, a3); } ), "doc" , pybind11::arg("measureIn"), pybind11::arg("selectIn"), pybind11::arg("massSetIn"), pybind11::arg("preclusterIn"));
		cl.def( pybind11::init<std::string, int, int, bool, bool>(), pybind11::arg("measureIn"), pybind11::arg("selectIn"), pybind11::arg("massSetIn"), pybind11::arg("preclusterIn"), pybind11::arg("reassignIn") );

		cl.def("analyze", [](Pythia8::ClusterJet &o, const class Pythia8::Event & a0, double const & a1, double const & a2) -> bool { return o.analyze(a0, a1, a2); }, "", pybind11::arg("event"), pybind11::arg("yScaleIn"), pybind11::arg("pTscaleIn"));
		cl.def("analyze", [](Pythia8::ClusterJet &o, const class Pythia8::Event & a0, double const & a1, double const & a2, int const & a3) -> bool { return o.analyze(a0, a1, a2, a3); }, "", pybind11::arg("event"), pybind11::arg("yScaleIn"), pybind11::arg("pTscaleIn"), pybind11::arg("nJetMinIn"));
		cl.def("analyze", (bool (Pythia8::ClusterJet::*)(const class Pythia8::Event &, double, double, int, int)) &Pythia8::ClusterJet::analyze, "C++: Pythia8::ClusterJet::analyze(const class Pythia8::Event &, double, double, int, int) --> bool", pybind11::arg("event"), pybind11::arg("yScaleIn"), pybind11::arg("pTscaleIn"), pybind11::arg("nJetMinIn"), pybind11::arg("nJetMaxIn"));
		cl.def("size", (int (Pythia8::ClusterJet::*)() const) &Pythia8::ClusterJet::size, "C++: Pythia8::ClusterJet::size() const --> int");
		cl.def("p", (class Pythia8::Vec4 (Pythia8::ClusterJet::*)(int) const) &Pythia8::ClusterJet::p, "C++: Pythia8::ClusterJet::p(int) const --> class Pythia8::Vec4", pybind11::arg("i"));
		cl.def("mult", (int (Pythia8::ClusterJet::*)(int) const) &Pythia8::ClusterJet::mult, "C++: Pythia8::ClusterJet::mult(int) const --> int", pybind11::arg("i"));
		cl.def("jetAssignment", (int (Pythia8::ClusterJet::*)(int) const) &Pythia8::ClusterJet::jetAssignment, "C++: Pythia8::ClusterJet::jetAssignment(int) const --> int", pybind11::arg("i"));
		cl.def("list", (void (Pythia8::ClusterJet::*)() const) &Pythia8::ClusterJet::list, "C++: Pythia8::ClusterJet::list() const --> void");
		cl.def("distanceSize", (int (Pythia8::ClusterJet::*)() const) &Pythia8::ClusterJet::distanceSize, "C++: Pythia8::ClusterJet::distanceSize() const --> int");
		cl.def("distance", (double (Pythia8::ClusterJet::*)(int) const) &Pythia8::ClusterJet::distance, "C++: Pythia8::ClusterJet::distance(int) const --> double", pybind11::arg("i"));
		cl.def("nError", (int (Pythia8::ClusterJet::*)() const) &Pythia8::ClusterJet::nError, "C++: Pythia8::ClusterJet::nError() const --> int");
	}
	{ // Pythia8::CellJet file:Pythia8/Analysis.h line:307
		pybind11::class_<Pythia8::CellJet, std::shared_ptr<Pythia8::CellJet>> cl(M("Pythia8"), "CellJet", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::CellJet(); } ), "doc" );
		cl.def( pybind11::init( [](double const & a0){ return new Pythia8::CellJet(a0); } ), "doc" , pybind11::arg("etaMaxIn"));
		cl.def( pybind11::init( [](double const & a0, int const & a1){ return new Pythia8::CellJet(a0, a1); } ), "doc" , pybind11::arg("etaMaxIn"), pybind11::arg("nEtaIn"));
		cl.def( pybind11::init( [](double const & a0, int const & a1, int const & a2){ return new Pythia8::CellJet(a0, a1, a2); } ), "doc" , pybind11::arg("etaMaxIn"), pybind11::arg("nEtaIn"), pybind11::arg("nPhiIn"));
		cl.def( pybind11::init( [](double const & a0, int const & a1, int const & a2, int const & a3){ return new Pythia8::CellJet(a0, a1, a2, a3); } ), "doc" , pybind11::arg("etaMaxIn"), pybind11::arg("nEtaIn"), pybind11::arg("nPhiIn"), pybind11::arg("selectIn"));
		cl.def( pybind11::init( [](double const & a0, int const & a1, int const & a2, int const & a3, int const & a4){ return new Pythia8::CellJet(a0, a1, a2, a3, a4); } ), "doc" , pybind11::arg("etaMaxIn"), pybind11::arg("nEtaIn"), pybind11::arg("nPhiIn"), pybind11::arg("selectIn"), pybind11::arg("smearIn"));
		cl.def( pybind11::init( [](double const & a0, int const & a1, int const & a2, int const & a3, int const & a4, double const & a5){ return new Pythia8::CellJet(a0, a1, a2, a3, a4, a5); } ), "doc" , pybind11::arg("etaMaxIn"), pybind11::arg("nEtaIn"), pybind11::arg("nPhiIn"), pybind11::arg("selectIn"), pybind11::arg("smearIn"), pybind11::arg("resolutionIn"));
		cl.def( pybind11::init( [](double const & a0, int const & a1, int const & a2, int const & a3, int const & a4, double const & a5, double const & a6){ return new Pythia8::CellJet(a0, a1, a2, a3, a4, a5, a6); } ), "doc" , pybind11::arg("etaMaxIn"), pybind11::arg("nEtaIn"), pybind11::arg("nPhiIn"), pybind11::arg("selectIn"), pybind11::arg("smearIn"), pybind11::arg("resolutionIn"), pybind11::arg("upperCutIn"));
		cl.def( pybind11::init( [](double const & a0, int const & a1, int const & a2, int const & a3, int const & a4, double const & a5, double const & a6, double const & a7){ return new Pythia8::CellJet(a0, a1, a2, a3, a4, a5, a6, a7); } ), "doc" , pybind11::arg("etaMaxIn"), pybind11::arg("nEtaIn"), pybind11::arg("nPhiIn"), pybind11::arg("selectIn"), pybind11::arg("smearIn"), pybind11::arg("resolutionIn"), pybind11::arg("upperCutIn"), pybind11::arg("thresholdIn"));
		cl.def( pybind11::init<double, int, int, int, int, double, double, double, class Pythia8::Rndm *>(), pybind11::arg("etaMaxIn"), pybind11::arg("nEtaIn"), pybind11::arg("nPhiIn"), pybind11::arg("selectIn"), pybind11::arg("smearIn"), pybind11::arg("resolutionIn"), pybind11::arg("upperCutIn"), pybind11::arg("thresholdIn"), pybind11::arg("rndmPtrIn") );

		cl.def("analyze", [](Pythia8::CellJet &o, const class Pythia8::Event & a0) -> bool { return o.analyze(a0); }, "", pybind11::arg("event"));
		cl.def("analyze", [](Pythia8::CellJet &o, const class Pythia8::Event & a0, double const & a1) -> bool { return o.analyze(a0, a1); }, "", pybind11::arg("event"), pybind11::arg("eTjetMinIn"));
		cl.def("analyze", [](Pythia8::CellJet &o, const class Pythia8::Event & a0, double const & a1, double const & a2) -> bool { return o.analyze(a0, a1, a2); }, "", pybind11::arg("event"), pybind11::arg("eTjetMinIn"), pybind11::arg("coneRadiusIn"));
		cl.def("analyze", (bool (Pythia8::CellJet::*)(const class Pythia8::Event &, double, double, double)) &Pythia8::CellJet::analyze, "C++: Pythia8::CellJet::analyze(const class Pythia8::Event &, double, double, double) --> bool", pybind11::arg("event"), pybind11::arg("eTjetMinIn"), pybind11::arg("coneRadiusIn"), pybind11::arg("eTseedIn"));
		cl.def("size", (int (Pythia8::CellJet::*)() const) &Pythia8::CellJet::size, "C++: Pythia8::CellJet::size() const --> int");
		cl.def("eT", (double (Pythia8::CellJet::*)(int) const) &Pythia8::CellJet::eT, "C++: Pythia8::CellJet::eT(int) const --> double", pybind11::arg("i"));
		cl.def("etaCenter", (double (Pythia8::CellJet::*)(int) const) &Pythia8::CellJet::etaCenter, "C++: Pythia8::CellJet::etaCenter(int) const --> double", pybind11::arg("i"));
		cl.def("phiCenter", (double (Pythia8::CellJet::*)(int) const) &Pythia8::CellJet::phiCenter, "C++: Pythia8::CellJet::phiCenter(int) const --> double", pybind11::arg("i"));
		cl.def("etaWeighted", (double (Pythia8::CellJet::*)(int) const) &Pythia8::CellJet::etaWeighted, "C++: Pythia8::CellJet::etaWeighted(int) const --> double", pybind11::arg("i"));
		cl.def("phiWeighted", (double (Pythia8::CellJet::*)(int) const) &Pythia8::CellJet::phiWeighted, "C++: Pythia8::CellJet::phiWeighted(int) const --> double", pybind11::arg("i"));
		cl.def("multiplicity", (int (Pythia8::CellJet::*)(int) const) &Pythia8::CellJet::multiplicity, "C++: Pythia8::CellJet::multiplicity(int) const --> int", pybind11::arg("i"));
		cl.def("pMassless", (class Pythia8::Vec4 (Pythia8::CellJet::*)(int) const) &Pythia8::CellJet::pMassless, "C++: Pythia8::CellJet::pMassless(int) const --> class Pythia8::Vec4", pybind11::arg("i"));
		cl.def("pMassive", (class Pythia8::Vec4 (Pythia8::CellJet::*)(int) const) &Pythia8::CellJet::pMassive, "C++: Pythia8::CellJet::pMassive(int) const --> class Pythia8::Vec4", pybind11::arg("i"));
		cl.def("m", (double (Pythia8::CellJet::*)(int) const) &Pythia8::CellJet::m, "C++: Pythia8::CellJet::m(int) const --> double", pybind11::arg("i"));
		cl.def("list", (void (Pythia8::CellJet::*)() const) &Pythia8::CellJet::list, "C++: Pythia8::CellJet::list() const --> void");
		cl.def("nError", (int (Pythia8::CellJet::*)() const) &Pythia8::CellJet::nError, "C++: Pythia8::CellJet::nError() const --> int");
	}
	{ // Pythia8::SlowJetHook file:Pythia8/Analysis.h line:371
		pybind11::class_<Pythia8::SlowJetHook, std::shared_ptr<Pythia8::SlowJetHook>, PyCallBack_Pythia8_SlowJetHook> cl(M("Pythia8"), "SlowJetHook", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new PyCallBack_Pythia8_SlowJetHook(); } ) );
		cl.def("include", (bool (Pythia8::SlowJetHook::*)(int, const class Pythia8::Event &, class Pythia8::Vec4 &, double &)) &Pythia8::SlowJetHook::include, "C++: Pythia8::SlowJetHook::include(int, const class Pythia8::Event &, class Pythia8::Vec4 &, double &) --> bool", pybind11::arg("iSel"), pybind11::arg("event"), pybind11::arg("pSel"), pybind11::arg("mSel"));
		cl.def("assign", (class Pythia8::SlowJetHook & (Pythia8::SlowJetHook::*)(const class Pythia8::SlowJetHook &)) &Pythia8::SlowJetHook::operator=, "C++: Pythia8::SlowJetHook::operator=(const class Pythia8::SlowJetHook &) --> class Pythia8::SlowJetHook &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::SlowJet file:Pythia8/Analysis.h line:422
		pybind11::class_<Pythia8::SlowJet, std::shared_ptr<Pythia8::SlowJet>, PyCallBack_Pythia8_SlowJet> cl(M("Pythia8"), "SlowJet", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](int const & a0, double const & a1){ return new Pythia8::SlowJet(a0, a1); }, [](int const & a0, double const & a1){ return new PyCallBack_Pythia8_SlowJet(a0, a1); } ), "doc");
		cl.def( pybind11::init( [](int const & a0, double const & a1, double const & a2){ return new Pythia8::SlowJet(a0, a1, a2); }, [](int const & a0, double const & a1, double const & a2){ return new PyCallBack_Pythia8_SlowJet(a0, a1, a2); } ), "doc");
		cl.def( pybind11::init( [](int const & a0, double const & a1, double const & a2, double const & a3){ return new Pythia8::SlowJet(a0, a1, a2, a3); }, [](int const & a0, double const & a1, double const & a2, double const & a3){ return new PyCallBack_Pythia8_SlowJet(a0, a1, a2, a3); } ), "doc");
		cl.def( pybind11::init( [](int const & a0, double const & a1, double const & a2, double const & a3, int const & a4){ return new Pythia8::SlowJet(a0, a1, a2, a3, a4); }, [](int const & a0, double const & a1, double const & a2, double const & a3, int const & a4){ return new PyCallBack_Pythia8_SlowJet(a0, a1, a2, a3, a4); } ), "doc");
		cl.def( pybind11::init( [](int const & a0, double const & a1, double const & a2, double const & a3, int const & a4, int const & a5){ return new Pythia8::SlowJet(a0, a1, a2, a3, a4, a5); }, [](int const & a0, double const & a1, double const & a2, double const & a3, int const & a4, int const & a5){ return new PyCallBack_Pythia8_SlowJet(a0, a1, a2, a3, a4, a5); } ), "doc");
		cl.def( pybind11::init( [](int const & a0, double const & a1, double const & a2, double const & a3, int const & a4, int const & a5, class Pythia8::SlowJetHook * a6){ return new Pythia8::SlowJet(a0, a1, a2, a3, a4, a5, a6); }, [](int const & a0, double const & a1, double const & a2, double const & a3, int const & a4, int const & a5, class Pythia8::SlowJetHook * a6){ return new PyCallBack_Pythia8_SlowJet(a0, a1, a2, a3, a4, a5, a6); } ), "doc");
		cl.def( pybind11::init( [](int const & a0, double const & a1, double const & a2, double const & a3, int const & a4, int const & a5, class Pythia8::SlowJetHook * a6, bool const & a7){ return new Pythia8::SlowJet(a0, a1, a2, a3, a4, a5, a6, a7); }, [](int const & a0, double const & a1, double const & a2, double const & a3, int const & a4, int const & a5, class Pythia8::SlowJetHook * a6, bool const & a7){ return new PyCallBack_Pythia8_SlowJet(a0, a1, a2, a3, a4, a5, a6, a7); } ), "doc");
		cl.def( pybind11::init<int, double, double, double, int, int, class Pythia8::SlowJetHook *, bool, bool>(), pybind11::arg("powerIn"), pybind11::arg("Rin"), pybind11::arg("pTjetMinIn"), pybind11::arg("etaMaxIn"), pybind11::arg("selectIn"), pybind11::arg("massSetIn"), pybind11::arg("sjHookPtrIn"), pybind11::arg("useFJcoreIn"), pybind11::arg("useStandardRin") );

		cl.def_readwrite("power", &Pythia8::SlowJet::power);
		cl.def_readwrite("R", &Pythia8::SlowJet::R);
		cl.def_readwrite("pTjetMin", &Pythia8::SlowJet::pTjetMin);
		cl.def_readwrite("etaMax", &Pythia8::SlowJet::etaMax);
		cl.def_readwrite("R2", &Pythia8::SlowJet::R2);
		cl.def_readwrite("pT2jetMin", &Pythia8::SlowJet::pT2jetMin);
		cl.def_readwrite("select", &Pythia8::SlowJet::select);
		cl.def_readwrite("massSet", &Pythia8::SlowJet::massSet);
		cl.def_readwrite("useFJcore", &Pythia8::SlowJet::useFJcore);
		cl.def_readwrite("useStandardR", &Pythia8::SlowJet::useStandardR);
		cl.def_readwrite("isAnti", &Pythia8::SlowJet::isAnti);
		cl.def_readwrite("isKT", &Pythia8::SlowJet::isKT);
		cl.def_readwrite("cutInEta", &Pythia8::SlowJet::cutInEta);
		cl.def_readwrite("chargedOnly", &Pythia8::SlowJet::chargedOnly);
		cl.def_readwrite("visibleOnly", &Pythia8::SlowJet::visibleOnly);
		cl.def_readwrite("modifyMass", &Pythia8::SlowJet::modifyMass);
		cl.def_readwrite("noHook", &Pythia8::SlowJet::noHook);
		cl.def_readwrite("clusters", &Pythia8::SlowJet::clusters);
		cl.def_readwrite("jets", &Pythia8::SlowJet::jets);
		cl.def_readwrite("diB", &Pythia8::SlowJet::diB);
		cl.def_readwrite("dij", &Pythia8::SlowJet::dij);
		cl.def_readwrite("origSize", &Pythia8::SlowJet::origSize);
		cl.def_readwrite("clSize", &Pythia8::SlowJet::clSize);
		cl.def_readwrite("clLast", &Pythia8::SlowJet::clLast);
		cl.def_readwrite("jtSize", &Pythia8::SlowJet::jtSize);
		cl.def_readwrite("iMin", &Pythia8::SlowJet::iMin);
		cl.def_readwrite("jMin", &Pythia8::SlowJet::jMin);
		cl.def_readwrite("dPhi", &Pythia8::SlowJet::dPhi);
		cl.def_readwrite("dijTemp", &Pythia8::SlowJet::dijTemp);
		cl.def_readwrite("dMin", &Pythia8::SlowJet::dMin);
		cl.def("analyze", (bool (Pythia8::SlowJet::*)(const class Pythia8::Event &)) &Pythia8::SlowJet::analyze, "C++: Pythia8::SlowJet::analyze(const class Pythia8::Event &) --> bool", pybind11::arg("event"));
		cl.def("setup", (bool (Pythia8::SlowJet::*)(const class Pythia8::Event &)) &Pythia8::SlowJet::setup, "C++: Pythia8::SlowJet::setup(const class Pythia8::Event &) --> bool", pybind11::arg("event"));
		cl.def("doStep", (bool (Pythia8::SlowJet::*)()) &Pythia8::SlowJet::doStep, "C++: Pythia8::SlowJet::doStep() --> bool");
		cl.def("doNSteps", (bool (Pythia8::SlowJet::*)(int)) &Pythia8::SlowJet::doNSteps, "C++: Pythia8::SlowJet::doNSteps(int) --> bool", pybind11::arg("nStep"));
		cl.def("stopAtN", (bool (Pythia8::SlowJet::*)(int)) &Pythia8::SlowJet::stopAtN, "C++: Pythia8::SlowJet::stopAtN(int) --> bool", pybind11::arg("nStop"));
		cl.def("sizeOrig", (int (Pythia8::SlowJet::*)() const) &Pythia8::SlowJet::sizeOrig, "C++: Pythia8::SlowJet::sizeOrig() const --> int");
		cl.def("sizeJet", (int (Pythia8::SlowJet::*)() const) &Pythia8::SlowJet::sizeJet, "C++: Pythia8::SlowJet::sizeJet() const --> int");
		cl.def("sizeAll", (int (Pythia8::SlowJet::*)() const) &Pythia8::SlowJet::sizeAll, "C++: Pythia8::SlowJet::sizeAll() const --> int");
		cl.def("pT", (double (Pythia8::SlowJet::*)(int) const) &Pythia8::SlowJet::pT, "C++: Pythia8::SlowJet::pT(int) const --> double", pybind11::arg("i"));
		cl.def("y", (double (Pythia8::SlowJet::*)(int) const) &Pythia8::SlowJet::y, "C++: Pythia8::SlowJet::y(int) const --> double", pybind11::arg("i"));
		cl.def("phi", (double (Pythia8::SlowJet::*)(int) const) &Pythia8::SlowJet::phi, "C++: Pythia8::SlowJet::phi(int) const --> double", pybind11::arg("i"));
		cl.def("p", (class Pythia8::Vec4 (Pythia8::SlowJet::*)(int) const) &Pythia8::SlowJet::p, "C++: Pythia8::SlowJet::p(int) const --> class Pythia8::Vec4", pybind11::arg("i"));
		cl.def("m", (double (Pythia8::SlowJet::*)(int) const) &Pythia8::SlowJet::m, "C++: Pythia8::SlowJet::m(int) const --> double", pybind11::arg("i"));
		cl.def("multiplicity", (int (Pythia8::SlowJet::*)(int) const) &Pythia8::SlowJet::multiplicity, "C++: Pythia8::SlowJet::multiplicity(int) const --> int", pybind11::arg("i"));
		cl.def("iNext", (int (Pythia8::SlowJet::*)() const) &Pythia8::SlowJet::iNext, "C++: Pythia8::SlowJet::iNext() const --> int");
		cl.def("jNext", (int (Pythia8::SlowJet::*)() const) &Pythia8::SlowJet::jNext, "C++: Pythia8::SlowJet::jNext() const --> int");
		cl.def("dNext", (double (Pythia8::SlowJet::*)() const) &Pythia8::SlowJet::dNext, "C++: Pythia8::SlowJet::dNext() const --> double");
		cl.def("list", [](Pythia8::SlowJet const &o) -> void { return o.list(); }, "");
		cl.def("list", (void (Pythia8::SlowJet::*)(bool) const) &Pythia8::SlowJet::list, "C++: Pythia8::SlowJet::list(bool) const --> void", pybind11::arg("listAll"));
		cl.def("constituents", (class std::vector<int, class std::allocator<int> > (Pythia8::SlowJet::*)(int)) &Pythia8::SlowJet::constituents, "C++: Pythia8::SlowJet::constituents(int) --> class std::vector<int, class std::allocator<int> >", pybind11::arg("j"));
		cl.def("clusConstituents", (class std::vector<int, class std::allocator<int> > (Pythia8::SlowJet::*)(int)) &Pythia8::SlowJet::clusConstituents, "C++: Pythia8::SlowJet::clusConstituents(int) --> class std::vector<int, class std::allocator<int> >", pybind11::arg("j"));
		cl.def("jetAssignment", (int (Pythia8::SlowJet::*)(int)) &Pythia8::SlowJet::jetAssignment, "C++: Pythia8::SlowJet::jetAssignment(int) --> int", pybind11::arg("i"));
		cl.def("removeJet", (void (Pythia8::SlowJet::*)(int)) &Pythia8::SlowJet::removeJet, "C++: Pythia8::SlowJet::removeJet(int) --> void", pybind11::arg("i"));
		cl.def("findNext", (void (Pythia8::SlowJet::*)()) &Pythia8::SlowJet::findNext, "C++: Pythia8::SlowJet::findNext() --> void");
		cl.def("clusterFJ", (bool (Pythia8::SlowJet::*)()) &Pythia8::SlowJet::clusterFJ, "C++: Pythia8::SlowJet::clusterFJ() --> bool");
		cl.def("assign", (class Pythia8::SlowJet & (Pythia8::SlowJet::*)(const class Pythia8::SlowJet &)) &Pythia8::SlowJet::operator=, "C++: Pythia8::SlowJet::operator=(const class Pythia8::SlowJet &) --> class Pythia8::SlowJet &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
}
