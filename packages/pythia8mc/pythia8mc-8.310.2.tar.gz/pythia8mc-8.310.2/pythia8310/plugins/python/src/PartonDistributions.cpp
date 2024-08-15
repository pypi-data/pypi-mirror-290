#include <Pythia8/Basics.h>
#include <Pythia8/BeamParticle.h>
#include <Pythia8/BeamSetup.h>
#include <Pythia8/BeamShape.h>
#include <Pythia8/BoseEinstein.h>
#include <Pythia8/ColourTracing.h>
#include <Pythia8/DeuteronProduction.h>
#include <Pythia8/Event.h>
#include <Pythia8/FragmentationFlavZpT.h>
#include <Pythia8/FragmentationSystems.h>
#include <Pythia8/HadronWidths.h>
#include <Pythia8/Info.h>
#include <Pythia8/LHEF3.h>
#include <Pythia8/Logger.h>
#include <Pythia8/MiniStringFragmentation.h>
#include <Pythia8/NucleonExcitations.h>
#include <Pythia8/ParticleData.h>
#include <Pythia8/PartonDistributions.h>
#include <Pythia8/PartonSystems.h>
#include <Pythia8/Ropewalk.h>
#include <Pythia8/Settings.h>
#include <Pythia8/SigmaLowEnergy.h>
#include <Pythia8/SigmaTotal.h>
#include <Pythia8/StandardModel.h>
#include <Pythia8/StringInteractions.h>
#include <Pythia8/SusyCouplings.h>
#include <Pythia8/Weights.h>
#include <cwchar>
#include <functional>
#include <ios>
#include <istream>
#include <iterator>
#include <map>
#include <memory>
#include <ostream>
#include <set>
#include <sstream> // __str__
#include <streambuf>
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

// Pythia8::PDF file:Pythia8/PartonDistributions.h line:49
struct PyCallBack_Pythia8_PDF : public Pythia8::PDF {
	using Pythia8::PDF::PDF;

	void setBeamID(int a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "setBeamID");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PDF::setBeamID(a0);
	}
	void setExtrapolate(bool a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "setExtrapolate");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PDF::setExtrapolate(a0);
	}
	bool insideBounds(double a0, double a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "insideBounds");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return PDF::insideBounds(a0, a1);
	}
	double alphaS(double a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "alphaS");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::alphaS(a0);
	}
	double mQuarkPDF(int a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "mQuarkPDF");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::mQuarkPDF(a0);
	}
	int nMembers() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "nMembers");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<int>::value) {
				static pybind11::detail::override_caster_t<int> caster;
				return pybind11::detail::cast_ref<int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<int>(std::move(o));
		}
		return PDF::nMembers();
	}
	void calcPDFEnvelope(int a0, double a1, double a2, int a3) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "calcPDFEnvelope");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PDF::calcPDFEnvelope(a0, a1, a2, a3);
	}
	void calcPDFEnvelope(struct std::pair<int, int> a0, struct std::pair<double, double> a1, double a2, int a3) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "calcPDFEnvelope");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2, a3);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PDF::calcPDFEnvelope(a0, a1, a2, a3);
	}
	struct Pythia8::PDF::PDFEnvelope getPDFEnvelope() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "getPDFEnvelope");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<struct Pythia8::PDF::PDFEnvelope>::value) {
				static pybind11::detail::override_caster_t<struct Pythia8::PDF::PDFEnvelope> caster;
				return pybind11::detail::cast_ref<struct Pythia8::PDF::PDFEnvelope>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<struct Pythia8::PDF::PDFEnvelope>(std::move(o));
		}
		return PDF::getPDFEnvelope();
	}
	double gammaPDFxDependence(int a0, double a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "gammaPDFxDependence");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::gammaPDFxDependence(a0, a1);
	}
	double gammaPDFRefScale(int a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "gammaPDFRefScale");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::gammaPDFRefScale(a0);
	}
	int sampleGammaValFlavor(double a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "sampleGammaValFlavor");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<int>::value) {
				static pybind11::detail::override_caster_t<int> caster;
				return pybind11::detail::cast_ref<int>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<int>(std::move(o));
		}
		return PDF::sampleGammaValFlavor(a0);
	}
	double xfIntegratedTotal(double a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "xfIntegratedTotal");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::xfIntegratedTotal(a0);
	}
	double xGamma() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "xGamma");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::xGamma();
	}
	void xPom(double a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "xPom");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PDF::xPom(a0);
	}
	double xfFlux(int a0, double a1, double a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "xfFlux");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::xfFlux(a0, a1, a2);
	}
	double xfApprox(int a0, double a1, double a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "xfApprox");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::xfApprox(a0, a1, a2);
	}
	double xfGamma(int a0, double a1, double a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "xfGamma");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::xfGamma(a0, a1, a2);
	}
	double intFluxApprox() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "intFluxApprox");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::intFluxApprox();
	}
	bool hasApproxGammaFlux() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "hasApproxGammaFlux");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<bool>::value) {
				static pybind11::detail::override_caster_t<bool> caster;
				return pybind11::detail::cast_ref<bool>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<bool>(std::move(o));
		}
		return PDF::hasApproxGammaFlux();
	}
	double getXmin() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "getXmin");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::getXmin();
	}
	double getXhadr() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "getXhadr");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::getXhadr();
	}
	double sampleXgamma(double a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "sampleXgamma");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::sampleXgamma(a0);
	}
	double sampleQ2gamma(double a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "sampleQ2gamma");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::sampleQ2gamma(a0);
	}
	double fluxQ2dependence(double a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "fluxQ2dependence");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::fluxQ2dependence(a0);
	}
	double xfMax(int a0, double a1, double a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "xfMax");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::xfMax(a0, a1, a2);
	}
	double xfSame(int a0, double a1, double a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "xfSame");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<double>::value) {
				static pybind11::detail::override_caster_t<double> caster;
				return pybind11::detail::cast_ref<double>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<double>(std::move(o));
		}
		return PDF::xfSame(a0, a1, a2);
	}
	void setVMDscale(double a0) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "setVMDscale");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return PDF::setVMDscale(a0);
	}
	void xfUpdate(int a0, double a1, double a2) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::PDF *>(this), "xfUpdate");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1, a2);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		pybind11::pybind11_fail("Tried to call pure virtual function \"PDF::xfUpdate\"");
	}
};

// Pythia8::BeamShape file:Pythia8/BeamShape.h line:21
struct PyCallBack_Pythia8_BeamShape : public Pythia8::BeamShape {
	using Pythia8::BeamShape::BeamShape;

	void init(class Pythia8::Settings & a0, class Pythia8::Rndm * a1) override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::BeamShape *>(this), "init");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>(a0, a1);
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return BeamShape::init(a0, a1);
	}
	void pick() override { 
		pybind11::gil_scoped_acquire gil;
		pybind11::function overload = pybind11::get_overload(static_cast<const Pythia8::BeamShape *>(this), "pick");
		if (overload) {
			auto o = overload.operator()<pybind11::return_value_policy::reference>();
			if (pybind11::detail::cast_is_temporary_value_reference<void>::value) {
				static pybind11::detail::override_caster_t<void> caster;
				return pybind11::detail::cast_ref<void>(std::move(o), caster);
			}
			else return pybind11::detail::cast_safe<void>(std::move(o));
		}
		return BeamShape::pick();
	}
};

void bind_Pythia8_PartonDistributions(std::function< pybind11::module &(std::string const &namespace_) > &M)
{
	{ // Pythia8::PDF file:Pythia8/PartonDistributions.h line:49
		pybind11::class_<Pythia8::PDF, std::shared_ptr<Pythia8::PDF>, PyCallBack_Pythia8_PDF> cl(M("Pythia8"), "PDF", "");
		pybind11::handle cl_type = cl;

		{ // Pythia8::PDF::PDFEnvelope file:Pythia8/PartonDistributions.h line:102
			auto & enclosing_class = cl;
			pybind11::class_<Pythia8::PDF::PDFEnvelope, std::shared_ptr<Pythia8::PDF::PDFEnvelope>> cl(enclosing_class, "PDFEnvelope", "");
			pybind11::handle cl_type = cl;

			cl.def( pybind11::init( [](){ return new Pythia8::PDF::PDFEnvelope(); } ) );
			cl.def( pybind11::init( [](Pythia8::PDF::PDFEnvelope const &o){ return new Pythia8::PDF::PDFEnvelope(o); } ) );
			cl.def_readwrite("centralPDF", &Pythia8::PDF::PDFEnvelope::centralPDF);
			cl.def_readwrite("errplusPDF", &Pythia8::PDF::PDFEnvelope::errplusPDF);
			cl.def_readwrite("errminusPDF", &Pythia8::PDF::PDFEnvelope::errminusPDF);
			cl.def_readwrite("errsymmPDF", &Pythia8::PDF::PDFEnvelope::errsymmPDF);
			cl.def_readwrite("scalePDF", &Pythia8::PDF::PDFEnvelope::scalePDF);
			cl.def_readwrite("pdfMemberVars", &Pythia8::PDF::PDFEnvelope::pdfMemberVars);
		}

		cl.def( pybind11::init( [](){ return new PyCallBack_Pythia8_PDF(); } ), "doc");
		cl.def( pybind11::init<int>(), pybind11::arg("idBeamIn") );

		cl.def(pybind11::init<PyCallBack_Pythia8_PDF const &>());
		cl.def_readwrite("idBeam", &Pythia8::PDF::idBeam);
		cl.def_readwrite("idBeamAbs", &Pythia8::PDF::idBeamAbs);
		cl.def_readwrite("idSav", &Pythia8::PDF::idSav);
		cl.def_readwrite("idVal1", &Pythia8::PDF::idVal1);
		cl.def_readwrite("idVal2", &Pythia8::PDF::idVal2);
		cl.def_readwrite("idVal3", &Pythia8::PDF::idVal3);
		cl.def_readwrite("xSav", &Pythia8::PDF::xSav);
		cl.def_readwrite("Q2Sav", &Pythia8::PDF::Q2Sav);
		cl.def_readwrite("xu", &Pythia8::PDF::xu);
		cl.def_readwrite("xd", &Pythia8::PDF::xd);
		cl.def_readwrite("xs", &Pythia8::PDF::xs);
		cl.def_readwrite("xubar", &Pythia8::PDF::xubar);
		cl.def_readwrite("xdbar", &Pythia8::PDF::xdbar);
		cl.def_readwrite("xsbar", &Pythia8::PDF::xsbar);
		cl.def_readwrite("xc", &Pythia8::PDF::xc);
		cl.def_readwrite("xb", &Pythia8::PDF::xb);
		cl.def_readwrite("xcbar", &Pythia8::PDF::xcbar);
		cl.def_readwrite("xbbar", &Pythia8::PDF::xbbar);
		cl.def_readwrite("xg", &Pythia8::PDF::xg);
		cl.def_readwrite("xlepton", &Pythia8::PDF::xlepton);
		cl.def_readwrite("xgamma", &Pythia8::PDF::xgamma);
		cl.def_readwrite("isSet", &Pythia8::PDF::isSet);
		cl.def_readwrite("isInit", &Pythia8::PDF::isInit);
		cl.def_readwrite("beamType", &Pythia8::PDF::beamType);
		cl.def_readwrite("hasGammaInLepton", &Pythia8::PDF::hasGammaInLepton);
		cl.def_readwrite("sSymmetricSave", &Pythia8::PDF::sSymmetricSave);
		cl.def_readwrite("cSymmetricSave", &Pythia8::PDF::cSymmetricSave);
		cl.def_readwrite("bSymmetricSave", &Pythia8::PDF::bSymmetricSave);
		cl.def("isSetup", (bool (Pythia8::PDF::*)()) &Pythia8::PDF::isSetup, "C++: Pythia8::PDF::isSetup() --> bool");
		cl.def("setBeamID", (void (Pythia8::PDF::*)(int)) &Pythia8::PDF::setBeamID, "C++: Pythia8::PDF::setBeamID(int) --> void", pybind11::arg("idBeamIn"));
		cl.def("resetValenceContent", (void (Pythia8::PDF::*)()) &Pythia8::PDF::resetValenceContent, "C++: Pythia8::PDF::resetValenceContent() --> void");
		cl.def("setValenceContent", (void (Pythia8::PDF::*)(int, int, int)) &Pythia8::PDF::setValenceContent, "C++: Pythia8::PDF::setValenceContent(int, int, int) --> void", pybind11::arg("idVal1In"), pybind11::arg("idVal2In"), pybind11::arg("idVal3In"));
		cl.def("setExtrapolate", (void (Pythia8::PDF::*)(bool)) &Pythia8::PDF::setExtrapolate, "C++: Pythia8::PDF::setExtrapolate(bool) --> void", pybind11::arg(""));
		cl.def("xf", (double (Pythia8::PDF::*)(int, double, double)) &Pythia8::PDF::xf, "C++: Pythia8::PDF::xf(int, double, double) --> double", pybind11::arg("id"), pybind11::arg("x"), pybind11::arg("Q2"));
		cl.def("xfVal", (double (Pythia8::PDF::*)(int, double, double)) &Pythia8::PDF::xfVal, "C++: Pythia8::PDF::xfVal(int, double, double) --> double", pybind11::arg("id"), pybind11::arg("x"), pybind11::arg("Q2"));
		cl.def("xfSea", (double (Pythia8::PDF::*)(int, double, double)) &Pythia8::PDF::xfSea, "C++: Pythia8::PDF::xfSea(int, double, double) --> double", pybind11::arg("id"), pybind11::arg("x"), pybind11::arg("Q2"));
		cl.def("insideBounds", (bool (Pythia8::PDF::*)(double, double)) &Pythia8::PDF::insideBounds, "C++: Pythia8::PDF::insideBounds(double, double) --> bool", pybind11::arg(""), pybind11::arg(""));
		cl.def("alphaS", (double (Pythia8::PDF::*)(double)) &Pythia8::PDF::alphaS, "C++: Pythia8::PDF::alphaS(double) --> double", pybind11::arg(""));
		cl.def("mQuarkPDF", (double (Pythia8::PDF::*)(int)) &Pythia8::PDF::mQuarkPDF, "C++: Pythia8::PDF::mQuarkPDF(int) --> double", pybind11::arg(""));
		cl.def("nMembers", (int (Pythia8::PDF::*)()) &Pythia8::PDF::nMembers, "C++: Pythia8::PDF::nMembers() --> int");
		cl.def("calcPDFEnvelope", (void (Pythia8::PDF::*)(int, double, double, int)) &Pythia8::PDF::calcPDFEnvelope, "C++: Pythia8::PDF::calcPDFEnvelope(int, double, double, int) --> void", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("calcPDFEnvelope", (void (Pythia8::PDF::*)(struct std::pair<int, int>, struct std::pair<double, double>, double, int)) &Pythia8::PDF::calcPDFEnvelope, "C++: Pythia8::PDF::calcPDFEnvelope(struct std::pair<int, int>, struct std::pair<double, double>, double, int) --> void", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("getPDFEnvelope", (struct Pythia8::PDF::PDFEnvelope (Pythia8::PDF::*)()) &Pythia8::PDF::getPDFEnvelope, "C++: Pythia8::PDF::getPDFEnvelope() --> struct Pythia8::PDF::PDFEnvelope");
		cl.def("gammaPDFxDependence", (double (Pythia8::PDF::*)(int, double)) &Pythia8::PDF::gammaPDFxDependence, "C++: Pythia8::PDF::gammaPDFxDependence(int, double) --> double", pybind11::arg(""), pybind11::arg(""));
		cl.def("gammaPDFRefScale", (double (Pythia8::PDF::*)(int)) &Pythia8::PDF::gammaPDFRefScale, "C++: Pythia8::PDF::gammaPDFRefScale(int) --> double", pybind11::arg(""));
		cl.def("sampleGammaValFlavor", (int (Pythia8::PDF::*)(double)) &Pythia8::PDF::sampleGammaValFlavor, "C++: Pythia8::PDF::sampleGammaValFlavor(double) --> int", pybind11::arg(""));
		cl.def("xfIntegratedTotal", (double (Pythia8::PDF::*)(double)) &Pythia8::PDF::xfIntegratedTotal, "C++: Pythia8::PDF::xfIntegratedTotal(double) --> double", pybind11::arg(""));
		cl.def("xGamma", (double (Pythia8::PDF::*)()) &Pythia8::PDF::xGamma, "C++: Pythia8::PDF::xGamma() --> double");
		cl.def("xPom", [](Pythia8::PDF &o) -> void { return o.xPom(); }, "");
		cl.def("xPom", (void (Pythia8::PDF::*)(double)) &Pythia8::PDF::xPom, "C++: Pythia8::PDF::xPom(double) --> void", pybind11::arg(""));
		cl.def("xfFlux", (double (Pythia8::PDF::*)(int, double, double)) &Pythia8::PDF::xfFlux, "C++: Pythia8::PDF::xfFlux(int, double, double) --> double", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("xfApprox", (double (Pythia8::PDF::*)(int, double, double)) &Pythia8::PDF::xfApprox, "C++: Pythia8::PDF::xfApprox(int, double, double) --> double", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("xfGamma", (double (Pythia8::PDF::*)(int, double, double)) &Pythia8::PDF::xfGamma, "C++: Pythia8::PDF::xfGamma(int, double, double) --> double", pybind11::arg(""), pybind11::arg(""), pybind11::arg(""));
		cl.def("intFluxApprox", (double (Pythia8::PDF::*)()) &Pythia8::PDF::intFluxApprox, "C++: Pythia8::PDF::intFluxApprox() --> double");
		cl.def("hasApproxGammaFlux", (bool (Pythia8::PDF::*)()) &Pythia8::PDF::hasApproxGammaFlux, "C++: Pythia8::PDF::hasApproxGammaFlux() --> bool");
		cl.def("getXmin", (double (Pythia8::PDF::*)()) &Pythia8::PDF::getXmin, "C++: Pythia8::PDF::getXmin() --> double");
		cl.def("getXhadr", (double (Pythia8::PDF::*)()) &Pythia8::PDF::getXhadr, "C++: Pythia8::PDF::getXhadr() --> double");
		cl.def("sampleXgamma", (double (Pythia8::PDF::*)(double)) &Pythia8::PDF::sampleXgamma, "C++: Pythia8::PDF::sampleXgamma(double) --> double", pybind11::arg(""));
		cl.def("sampleQ2gamma", (double (Pythia8::PDF::*)(double)) &Pythia8::PDF::sampleQ2gamma, "C++: Pythia8::PDF::sampleQ2gamma(double) --> double", pybind11::arg(""));
		cl.def("fluxQ2dependence", (double (Pythia8::PDF::*)(double)) &Pythia8::PDF::fluxQ2dependence, "C++: Pythia8::PDF::fluxQ2dependence(double) --> double", pybind11::arg(""));
		cl.def("xfMax", (double (Pythia8::PDF::*)(int, double, double)) &Pythia8::PDF::xfMax, "C++: Pythia8::PDF::xfMax(int, double, double) --> double", pybind11::arg("id"), pybind11::arg("x"), pybind11::arg("Q2"));
		cl.def("xfSame", (double (Pythia8::PDF::*)(int, double, double)) &Pythia8::PDF::xfSame, "C++: Pythia8::PDF::xfSame(int, double, double) --> double", pybind11::arg("id"), pybind11::arg("x"), pybind11::arg("Q2"));
		cl.def("setVMDscale", [](Pythia8::PDF &o) -> void { return o.setVMDscale(); }, "");
		cl.def("setVMDscale", (void (Pythia8::PDF::*)(double)) &Pythia8::PDF::setVMDscale, "C++: Pythia8::PDF::setVMDscale(double) --> void", pybind11::arg(""));
		cl.def("sSymmetric", (bool (Pythia8::PDF::*)() const) &Pythia8::PDF::sSymmetric, "C++: Pythia8::PDF::sSymmetric() const --> bool");
		cl.def("cSymmetric", (bool (Pythia8::PDF::*)() const) &Pythia8::PDF::cSymmetric, "C++: Pythia8::PDF::cSymmetric() const --> bool");
		cl.def("bSymmetric", (bool (Pythia8::PDF::*)() const) &Pythia8::PDF::bSymmetric, "C++: Pythia8::PDF::bSymmetric() const --> bool");
		cl.def("sSymmetric", (void (Pythia8::PDF::*)(bool)) &Pythia8::PDF::sSymmetric, "C++: Pythia8::PDF::sSymmetric(bool) --> void", pybind11::arg("sSymmetricIn"));
		cl.def("cSymmetric", (void (Pythia8::PDF::*)(bool)) &Pythia8::PDF::cSymmetric, "C++: Pythia8::PDF::cSymmetric(bool) --> void", pybind11::arg("cSymmetricIn"));
		cl.def("bSymmetric", (void (Pythia8::PDF::*)(bool)) &Pythia8::PDF::bSymmetric, "C++: Pythia8::PDF::bSymmetric(bool) --> void", pybind11::arg("bSymmetricIn"));
		cl.def("xfUpdate", (void (Pythia8::PDF::*)(int, double, double)) &Pythia8::PDF::xfUpdate, "C++: Pythia8::PDF::xfUpdate(int, double, double) --> void", pybind11::arg("id"), pybind11::arg("x"), pybind11::arg("Q2"));
		cl.def("xfRaw", (double (Pythia8::PDF::*)(int) const) &Pythia8::PDF::xfRaw, "C++: Pythia8::PDF::xfRaw(int) const --> double", pybind11::arg("id"));
		cl.def("isValence", (bool (Pythia8::PDF::*)(int) const) &Pythia8::PDF::isValence, "C++: Pythia8::PDF::isValence(int) const --> bool", pybind11::arg("id"));
		cl.def("assign", (class Pythia8::PDF & (Pythia8::PDF::*)(const class Pythia8::PDF &)) &Pythia8::PDF::operator=, "C++: Pythia8::PDF::operator=(const class Pythia8::PDF &) --> class Pythia8::PDF &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
	{ // Pythia8::BeamShape file:Pythia8/BeamShape.h line:21
		pybind11::class_<Pythia8::BeamShape, std::shared_ptr<Pythia8::BeamShape>, PyCallBack_Pythia8_BeamShape> cl(M("Pythia8"), "BeamShape", "");
		pybind11::handle cl_type = cl;

		cl.def( pybind11::init( [](){ return new Pythia8::BeamShape(); }, [](){ return new PyCallBack_Pythia8_BeamShape(); } ) );
		cl.def_readwrite("deltaPxA", &Pythia8::BeamShape::deltaPxA);
		cl.def_readwrite("deltaPyA", &Pythia8::BeamShape::deltaPyA);
		cl.def_readwrite("deltaPzA", &Pythia8::BeamShape::deltaPzA);
		cl.def_readwrite("deltaPxB", &Pythia8::BeamShape::deltaPxB);
		cl.def_readwrite("deltaPyB", &Pythia8::BeamShape::deltaPyB);
		cl.def_readwrite("deltaPzB", &Pythia8::BeamShape::deltaPzB);
		cl.def_readwrite("vertexX", &Pythia8::BeamShape::vertexX);
		cl.def_readwrite("vertexY", &Pythia8::BeamShape::vertexY);
		cl.def_readwrite("vertexZ", &Pythia8::BeamShape::vertexZ);
		cl.def_readwrite("vertexT", &Pythia8::BeamShape::vertexT);
		cl.def_readwrite("allowMomentumSpread", &Pythia8::BeamShape::allowMomentumSpread);
		cl.def_readwrite("allowVertexSpread", &Pythia8::BeamShape::allowVertexSpread);
		cl.def_readwrite("sigmaPxA", &Pythia8::BeamShape::sigmaPxA);
		cl.def_readwrite("sigmaPyA", &Pythia8::BeamShape::sigmaPyA);
		cl.def_readwrite("sigmaPzA", &Pythia8::BeamShape::sigmaPzA);
		cl.def_readwrite("maxDevA", &Pythia8::BeamShape::maxDevA);
		cl.def_readwrite("sigmaPxB", &Pythia8::BeamShape::sigmaPxB);
		cl.def_readwrite("sigmaPyB", &Pythia8::BeamShape::sigmaPyB);
		cl.def_readwrite("sigmaPzB", &Pythia8::BeamShape::sigmaPzB);
		cl.def_readwrite("maxDevB", &Pythia8::BeamShape::maxDevB);
		cl.def_readwrite("sigmaVertexX", &Pythia8::BeamShape::sigmaVertexX);
		cl.def_readwrite("sigmaVertexY", &Pythia8::BeamShape::sigmaVertexY);
		cl.def_readwrite("sigmaVertexZ", &Pythia8::BeamShape::sigmaVertexZ);
		cl.def_readwrite("maxDevVertex", &Pythia8::BeamShape::maxDevVertex);
		cl.def_readwrite("sigmaTime", &Pythia8::BeamShape::sigmaTime);
		cl.def_readwrite("maxDevTime", &Pythia8::BeamShape::maxDevTime);
		cl.def_readwrite("offsetX", &Pythia8::BeamShape::offsetX);
		cl.def_readwrite("offsetY", &Pythia8::BeamShape::offsetY);
		cl.def_readwrite("offsetZ", &Pythia8::BeamShape::offsetZ);
		cl.def_readwrite("offsetT", &Pythia8::BeamShape::offsetT);
		cl.def("init", (void (Pythia8::BeamShape::*)(class Pythia8::Settings &, class Pythia8::Rndm *)) &Pythia8::BeamShape::init, "C++: Pythia8::BeamShape::init(class Pythia8::Settings &, class Pythia8::Rndm *) --> void", pybind11::arg("settings"), pybind11::arg("rndmPtrIn"));
		cl.def("pick", (void (Pythia8::BeamShape::*)()) &Pythia8::BeamShape::pick, "C++: Pythia8::BeamShape::pick() --> void");
		cl.def("deltaPA", (class Pythia8::Vec4 (Pythia8::BeamShape::*)() const) &Pythia8::BeamShape::deltaPA, "C++: Pythia8::BeamShape::deltaPA() const --> class Pythia8::Vec4");
		cl.def("deltaPB", (class Pythia8::Vec4 (Pythia8::BeamShape::*)() const) &Pythia8::BeamShape::deltaPB, "C++: Pythia8::BeamShape::deltaPB() const --> class Pythia8::Vec4");
		cl.def("vertex", (class Pythia8::Vec4 (Pythia8::BeamShape::*)() const) &Pythia8::BeamShape::vertex, "C++: Pythia8::BeamShape::vertex() const --> class Pythia8::Vec4");
		cl.def("assign", (class Pythia8::BeamShape & (Pythia8::BeamShape::*)(const class Pythia8::BeamShape &)) &Pythia8::BeamShape::operator=, "C++: Pythia8::BeamShape::operator=(const class Pythia8::BeamShape &) --> class Pythia8::BeamShape &", pybind11::return_value_policy::reference, pybind11::arg(""));
	}
}
