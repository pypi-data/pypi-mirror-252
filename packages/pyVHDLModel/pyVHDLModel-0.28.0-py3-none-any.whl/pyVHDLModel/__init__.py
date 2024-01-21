# ==================================================================================================================== #
#             __     ___   _ ____  _     __  __           _      _                                                     #
#   _ __  _   \ \   / / | | |  _ \| |   |  \/  | ___   __| | ___| |                                                    #
#  | '_ \| | | \ \ / /| |_| | | | | |   | |\/| |/ _ \ / _` |/ _ \ |                                                    #
#  | |_) | |_| |\ V / |  _  | |_| | |___| |  | | (_) | (_| |  __/ |                                                    #
#  | .__/ \__, | \_/  |_| |_|____/|_____|_|  |_|\___/ \__,_|\___|_|                                                    #
#  |_|    |___/                                                                                                        #
# ==================================================================================================================== #
# Authors:                                                                                                             #
#   Patrick Lehmann                                                                                                    #
#                                                                                                                      #
# License:                                                                                                             #
# ==================================================================================================================== #
# Copyright 2017-2023 Patrick Lehmann - Boetzingen, Germany                                                            #
# Copyright 2016-2017 Patrick Lehmann - Dresden, Germany                                                               #
#                                                                                                                      #
# Licensed under the Apache License, Version 2.0 (the "License");                                                      #
# you may not use this file except in compliance with the License.                                                     #
# You may obtain a copy of the License at                                                                              #
#                                                                                                                      #
#   http://www.apache.org/licenses/LICENSE-2.0                                                                         #
#                                                                                                                      #
# Unless required by applicable law or agreed to in writing, software                                                  #
# distributed under the License is distributed on an "AS IS" BASIS,                                                    #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.                                             #
# See the License for the specific language governing permissions and                                                  #
# limitations under the License.                                                                                       #
#                                                                                                                      #
# SPDX-License-Identifier: Apache-2.0                                                                                  #
# ==================================================================================================================== #
#
"""
**An abstract VHDL language model.**

This package provides a unified abstract language model for VHDL. Projects reading from source files can derive own
classes and implement additional logic to create a concrete language model for their tools.

Projects consuming pre-processed VHDL data (parsed, analyzed or elaborated) can build higher level features and services
on such a model, while supporting multiple frontends.

.. admonition:: Copyright Information

   :copyright: Copyright 2017-2023 Patrick Lehmann - Bötzingen, Germany
   :copyright: Copyright 2016-2017 Patrick Lehmann - Dresden, Germany
   :license: Apache License, Version 2.0
"""
__author__ =    "Patrick Lehmann"
__email__ =     "Paebbels@gmail.com"
__copyright__ = "2016-2023, Patrick Lehmann"
__license__ =   "Apache License, Version 2.0"
__version__ =   "0.28.0"


from enum                      import unique, Enum, Flag, auto
from pathlib                   import Path

from typing                    import Union, Dict, cast, List, Generator, Optional as Nullable

from pyTooling.Decorators      import export
from pyTooling.Graph           import Graph, Vertex, Edge

from pyVHDLModel.Exception     import VHDLModelException
from pyVHDLModel.Exception     import LibraryExistsInDesignError, LibraryRegisteredToForeignDesignError, LibraryNotRegisteredError, EntityExistsInLibraryError
from pyVHDLModel.Exception     import ArchitectureExistsInLibraryError, PackageExistsInLibraryError, PackageBodyExistsError, ConfigurationExistsInLibraryError
from pyVHDLModel.Exception     import ContextExistsInLibraryError, ReferencedLibraryNotExistingError
from pyVHDLModel.Base          import ModelEntity, NamedEntityMixin, DocumentedEntityMixin
from pyVHDLModel.Expression    import UnaryExpression, BinaryExpression, TernaryExpression
from pyVHDLModel.Namespace     import Namespace
from pyVHDLModel.Object        import Obj, Signal, Constant, DeferredConstant
from pyVHDLModel.Symbol        import PackageReferenceSymbol, AllPackageMembersReferenceSymbol, PackageMemberReferenceSymbol, SimpleObjectOrFunctionCallSymbol
from pyVHDLModel.Concurrent    import EntityInstantiation, ComponentInstantiation, ConfigurationInstantiation
from pyVHDLModel.DesignUnit    import DesignUnit, PrimaryUnit, Architecture, PackageBody, Context, Entity, Configuration, Package
from pyVHDLModel.PSLModel      import VerificationUnit, VerificationProperty, VerificationMode
from pyVHDLModel.Instantiation import PackageInstantiation
from pyVHDLModel.Type          import IntegerType, PhysicalType, ArrayType, RecordType


@export
@unique
class VHDLVersion(Enum):
	"""
	An enumeration for all possible version numbers for VHDL and VHDL-AMS.

	A version can be given as integer or string and is represented as a unified
	enumeration value.

	This enumeration supports compare operators.
	"""

	Any =                -1  #: Any
	VHDL87 =             87  #: VHDL-1987
	VHDL93 =             93  #: VHDL-1993
	AMS93 =            1993  #: VHDL-AMS-1993
	AMS99 =            1999  #: VHDL-AMS-1999
	VHDL2000 =         2000  #: VHDL-2000
	VHDL2002 =         2002  #: VHDL-2002
	VHDL2008 =         2008  #: VHDL-2008
	AMS2017 =          2017  #: VHDL-AMS-2017
	VHDL2019 =         2019  #: VHDL-2019
	Latest =          10000  #: Latest VHDL (2019)

	__VERSION_MAPPINGS__: Dict[Union[int, str], Enum] = {
		-1:       Any,
		87:       VHDL87,
		93:       VHDL93,
		# 93:       AMS93,
		99:       AMS99,
		0:        VHDL2000,
		2:        VHDL2002,
		8:        VHDL2008,
		17:       AMS2017,
		19:       VHDL2019,
		1987:     VHDL87,
		# 1993:     VHDL93,
		1993:     AMS93,
		1999:     AMS99,
		2000:     VHDL2000,
		2002:     VHDL2002,
		2008:     VHDL2008,
		2017:     AMS2017,
		2019:     VHDL2019,
		10000:    Latest,
		"Any":    Any,
		"87":     VHDL87,
		"93":     VHDL93,
		# "93":     AMS93,
		"99":     AMS99,
		"00":     VHDL2000,
		"02":     VHDL2002,
		"08":     VHDL2008,
		"17":     AMS2017,
		"19":     VHDL2019,
		"1987":   VHDL87,
		# "1993":   VHDL93,
		"1993":   AMS93,
		"1999":   AMS99,
		"2000":   VHDL2000,
		"2002":   VHDL2002,
		"2008":   VHDL2008,
		"2017":   AMS2017,
		"2019":   VHDL2019,
		"Latest": Latest,
	}  #: Dictionary of VHDL and VHDL-AMS year codes variants as integer and strings for mapping to unique enum values.

	def __init__(self, *_) -> None:
		"""Patch the embedded MAP dictionary"""
		for k, v in self.__class__.__VERSION_MAPPINGS__.items():
			if (not isinstance(v, self.__class__)) and (v == self.value):
				self.__class__.__VERSION_MAPPINGS__[k] = self

	@classmethod
	def Parse(cls, value: Union[int, str]) -> "VHDLVersion":
		"""
		Parses a VHDL or VHDL-AMS year code as integer or string to an enum value.

		:param value:       VHDL/VHDL-AMS year code.
		:returns:           Enumeration value.
		:raises ValueError: If the year code is not recognized.
		"""
		try:
			return cls.__VERSION_MAPPINGS__[value]
		except KeyError:
			raise ValueError(f"Value '{value!s}' cannot be parsed to member of {cls.__name__}.")

	def __lt__(self, other: Any) -> bool:
		"""
		Compare two VHDL/VHDL-AMS versions if the version is less than the second operand.

		:param other:      Parameter to compare against.
		:returns:          True if version is less than the second operand.
		:raises TypeError: If parameter ``other`` is not of type :class:`VHDLVersion`.
		"""
		if isinstance(other, VHDLVersion):
			return self.value < other.value
		else:
			raise TypeError("Second operand is not of type 'VHDLVersion'.")

	def __le__(self, other: Any) -> bool:
		"""
		Compare two VHDL/VHDL-AMS versions if the version is less or equal than the second operand.

		:param other:      Parameter to compare against.
		:returns:          True if version is less or equal than the second operand.
		:raises TypeError: If parameter ``other`` is not of type :class:`VHDLVersion`.
		"""
		if isinstance(other, VHDLVersion):
			return self.value <= other.value
		else:
			raise TypeError("Second operand is not of type 'VHDLVersion'.")

	def __gt__(self, other: Any) -> bool:
		"""
		Compare two VHDL/VHDL-AMS versions if the version is greater than the second operand.

		:param other:      Parameter to compare against.
		:returns:          True if version is greater than the second operand.
		:raises TypeError: If parameter ``other`` is not of type :class:`VHDLVersion`.
		"""
		if isinstance(other, VHDLVersion):
			return self.value > other.value
		else:
			raise TypeError("Second operand is not of type 'VHDLVersion'.")

	def __ge__(self, other: Any) -> bool:
		"""
		Compare two VHDL/VHDL-AMS versions if the version is greater or equal than the second operand.

		:param other:      Parameter to compare against.
		:returns:          True if version is greater or equal than the second operand.
		:raises TypeError: If parameter ``other`` is not of type :class:`VHDLVersion`.
		"""
		if isinstance(other, VHDLVersion):
			return self.value >= other.value
		else:
			raise TypeError("Second operand is not of type 'VHDLVersion'.")

	def __ne__(self, other: Any) -> bool:
		"""
		Compare two VHDL/VHDL-AMS versions if the version is unequal to the second operand.

		:param other:      Parameter to compare against.
		:returns:          True if version is unequal to the second operand.
		:raises TypeError: If parameter ``other`` is not of type :class:`VHDLVersion`.
		"""
		if isinstance(other, VHDLVersion):
			return self.value != other.value
		else:
			raise TypeError("Second operand is not of type 'VHDLVersion'.")

	def __eq__(self, other: Any) -> bool:
		"""
		Compare two VHDL/VHDL-AMS versions if the version is equal to the second operand.

		:param other:      Parameter to compare against.
		:returns:          True if version is equal to the second operand.
		:raises TypeError: If parameter ``other`` is not of type :class:`VHDLVersion`.
		"""
		if isinstance(other, VHDLVersion):
			if (self is self.__class__.Any) or (other is self.__class__.Any):
				return True
			else:
				return self.value == other.value
		else:
			raise TypeError("Second operand is not of type 'VHDLVersion'.")

	@property
	def IsVHDL(self) -> bool:
		"""
		Checks if the version is a VHDL (not VHDL-AMS) version.

		:returns:          True if version is a VHDL version.
		"""
		return self in (self.VHDL87, self.VHDL93, self.VHDL2002, self.VHDL2008, self.VHDL2019)

	@property
	def IsAMS(self) -> bool:
		"""
		Checks if the version is a VHDL-AMS (not VHDL) version.

		:returns:          True if version is a VHDL-AMS version.
		"""
		return self in (self.AMS93, self.AMS99, self.AMS2017)

	def __str__(self) -> str:
		"""
		Formats the VHDL version to pattern ``VHDL'xx`` or in case of VHDL-AMS to ``VHDL-AMS'xx``.

		:return: Formatted VHDL/VHDL-AMS version.
		"""
		if self.value == self.Any.value:
			return "VHDL'Any"
		elif self.value == self.Latest.value:
			return "VHDL'Latest"

		year = str(self.value)[-2:]
		if self.IsVHDL:
			return f"VHDL'{year}"
		else:
			return f"VHDL-AMS'{year}"

	def __repr__(self) -> str:
		"""
		Formats the VHDL/VHDL-AMS version to pattern ``xxxx``.

		:return: Formatted VHDL/VHDL-AMS version.
		"""
		if self.value == self.Any.value:
			return "Any"
		elif self.value == self.Latest.value:
			return "Latest"
		else:
			return str(self.value)


@export
@unique
class ObjectClass(Enum):
	"""
	An ``ObjectClass`` is an enumeration. It represents an object's class (``constant``, ``signal``, ...).

	In case no *object class* is defined, ``Default`` is used, so the *object class* is inferred from context.
	"""

	Default =    0  #: Object class not defined, thus it's context dependent.
	Constant =   1  #: Constant
	Variable =   2  #: Variable
	Signal =     3  #: Signal
	File =       4  #: File
	Type =       5  #: Type
	# FIXME: Package?
	Procedure =  6  #: Procedure
	Function =   7  #: Function

	def __str__(self):
		"""
		Formats the object class.

		:return: Formatted object class.
		"""
		return ("", "constant", "variable", "signal", "file", "type", "procedure", "function")[cast(int, self.value)]       # TODO: check performance


@export
@unique
class DesignUnitKind(Flag):
	Context = auto()
	Package = auto()
	PackageBody = auto()
	Entity = auto()
	Architecture = auto()
	Configuration = auto()

	Primary = Context | Configuration | Entity | Package
	Secondary = PackageBody | Architecture
	WithContext = Configuration | Package | Entity | PackageBody | Architecture
	WithDeclaredItems = Package | Entity | PackageBody | Architecture

	All = Primary | Secondary


@export
@unique
class DependencyGraphVertexKind(Flag):
	Document = auto()
	Library = auto()

	Context = auto()
	Package = auto()
	PackageBody = auto()
	Entity = auto()
	Architecture = auto()
	Component = auto()
	Configuration = auto()


@export
@unique
class DependencyGraphEdgeKind(Flag):
	Document =       auto()
	Library =        auto()
	Context =        auto()
	Package =        auto()
	Entity =         auto()
	# Architecture = auto()
	Configuration =  auto()
	Component =      auto()

	DeclaredIn =     auto()
	Order =          auto()
	Reference =      auto()
	Implementation = auto()
	Instantiation =  auto()

	SourceFile =                 Document | DeclaredIn
	CompileOrder =               Document | Order

	LibraryClause =              Library | Reference
	UseClause =                  Package | Reference
	ContextReference =           Context | Reference

	EntityImplementation =       Entity | Implementation
	PackageImplementation =      Package | Implementation

	EntityInstantiation =        Entity | Instantiation
	ComponentInstantiation =     Component | Instantiation
	ConfigurationInstantiation = Configuration | Instantiation


@export
@unique
class ObjectGraphVertexKind(Flag):
	Type = auto()
	Subtype = auto()

	Constant = auto()
	DeferredConstant = auto()
	Variable = auto()
	Signal = auto()
	File = auto()

	Alias = auto()


@export
@unique
class ObjectGraphEdgeKind(Flag):
	BaseType = auto()
	Subtype = auto()

	ReferenceInExpression = auto()


@export
class Design(ModelEntity):
	"""
	A ``Design`` represents all loaded and analysed files (see :class:`~pyVHDLModel.Document`). It's the root of this
	document-object-model (DOM). It contains at least one VHDL library (see :class:`~pyVHDLModel.Library`).
	"""
	_name:              Nullable[str]         #: Name of the design
	_libraries:         Dict[str, 'Library']  #: List of all libraries defined for a design.
	_documents:         List['Document']      #: List of all documents loaded for a design.
	_dependencyGraph:   Graph[None, None, None, None, None, None, None, None, str, DesignUnit, None, None, None, None, None, None, None, None, None, None, None, None, None]   #: The graph of all dependencies in the designs.
	_compileOrderGraph: Graph[None, None, None, None, None, None, None, None, None, 'Document', None, None, None, None, None, None, None, None, None, None, None, None, None]  #: A graph derived from dependency graph containing the order of documents for compilation.
	_hierarchyGraph:    Graph[None, None, None, None, None, None, None, None, str, DesignUnit, None, None, None, None, None, None, None, None, None, None, None, None, None]   #: A graph derived from dependency graph containing the design hierarchy.
	_objectGraph:       Graph[None, None, None, None, None, None, None, None, str, Obj, None, None, None, None, None, None, None, None, None, None, None, None, None]       #: The graph of all types and objects in the design.
	_toplevel:          Union[Entity, Configuration]  #: When computed, the toplevel design unit is cached in this field.

	def __init__(self, name: str = None):
		"""
		Initializes a VHDL design.

		:param name: Name of the design.
		"""
		super().__init__()

		self._name =      name
		self._libraries = {}
		self._documents = []

		self._compileOrderGraph = Graph()
		self._dependencyGraph = Graph()
		self._hierarchyGraph = Graph()
		self._objectGraph = Graph()
		self._toplevel = None

	@property
	def Libraries(self) -> Dict[str, 'Library']:
		"""Returns a list of all libraries specified for this design."""
		return self._libraries

	@property
	def Documents(self) -> List['Document']:
		"""Returns a list of all documents (files) loaded for this design."""
		return self._documents

	@property
	def CompileOrderGraph(self) -> Graph:
		return self._compileOrderGraph

	@property
	def DependencyGraph(self) -> Graph:
		return self._dependencyGraph

	@property
	def HierarchyGraph(self) -> Graph:
		return self._hierarchyGraph

	@property
	def ObjectGraph(self) -> Graph:
		return self._objectGraph

	@property
	def TopLevel(self) -> 'Entity':
		# Check for cached result
		if self._toplevel is not None:
			return self._toplevel

		if self._hierarchyGraph.EdgeCount == 0:
			raise VHDLModelException(f"Hierarchy is not yet computed from dependency graph.")

		roots = tuple(self._hierarchyGraph.IterateRoots())
		if len(roots) == 1:
			toplevel = roots[0]
			self._hierarchyGraph["toplevel"] = toplevel
			self._toplevel = toplevel.Value
			return toplevel.Value
		else:
			raise VHDLModelException(f"Found more than one toplevel: {', '.join(roots)}")

	def _LoadLibrary(self, library: 'Library') -> None:
		libraryIdentifier = library.NormalizedIdentifier
		if libraryIdentifier in self._libraries:
			raise LibraryExistsInDesignError(library)

		self._libraries[libraryIdentifier] = library
		library._parent = self

	def LoadStdLibrary(self) -> 'Library':
		from pyVHDLModel.STD import Std

		doc = Document(Path("std.vhdl"))

		library = Std()
		for designUnit in library.IterateDesignUnits():
			doc._AddDesignUnit(designUnit)

		self._LoadLibrary(library)

		return library

	def LoadIEEELibrary(self) -> 'Library':
		from pyVHDLModel.IEEE import Ieee

		doc = Document(Path("ieee.vhdl"))

		library = Ieee()
		for designUnit in library.IterateDesignUnits():
			doc._AddDesignUnit(designUnit)

		self._LoadLibrary(library)

		return library

	def AddLibrary(self, library: 'Library') -> None:
		libraryIdentifier = library.NormalizedIdentifier
		if libraryIdentifier in self._libraries:
			raise LibraryExistsInDesignError(library)

		if library._parent is not None:
			raise LibraryRegisteredToForeignDesignError(library)

		self._libraries[libraryIdentifier] = library
		library._parent = self

	def GetLibrary(self, libraryName: str) -> 'Library':
		libraryIdentifier = libraryName.lower()
		try:
			return self._libraries[libraryIdentifier]
		except KeyError:
			lib = Library(libraryName)
			self._libraries[libraryIdentifier] = lib
			lib._parent = self
			return lib

	# TODO: allow overloaded parameter library to be str?
	def AddDocument(self, document: 'Document', library: 'Library') -> None:
		if library.NormalizedIdentifier not in self._libraries:
			raise LibraryNotRegisteredError(library)

		self._documents.append(document)
		document._parent = self

		for entityIdentifier, entity in document._entities.items():
			if entityIdentifier in library._entities:
				raise EntityExistsInLibraryError(entity, library)

			library._entities[entityIdentifier] = entity
			entity.Library = library

		for entityIdentifier, architectures in document._architectures.items():
			try:
				architecturesPerEntity = library._architectures[entityIdentifier]
				for architectureIdentifier, architecture in architectures.items():
					if architectureIdentifier in architecturesPerEntity:
						raise ArchitectureExistsInLibraryError(architecture, library._entities[entityIdentifier], library)

					architecturesPerEntity[architectureIdentifier] = architecture
					architecture.Library = library
			except KeyError:
				architecturesPerEntity = document._architectures[entityIdentifier].copy()
				library._architectures[entityIdentifier] = architecturesPerEntity

				for architecture in architecturesPerEntity.values():
					architecture.Library = library

		for packageIdentifier, package in document._packages.items():
			if packageIdentifier in library._packages:
				raise PackageExistsInLibraryError(package, library)

			library._packages[packageIdentifier] = package
			package.Library = library

		for packageBodyIdentifier, packageBody in document._packageBodies.items():
			if packageBodyIdentifier in library._packageBodies:
				raise PackageBodyExistsError(packageBody, library)

			library._packageBodies[packageBodyIdentifier] = packageBody
			packageBody.Library = library

		for configurationIdentifier, configuration in document._configurations.items():
			if configurationIdentifier in library._configurations:
				raise ConfigurationExistsInLibraryError(configuration, library)

			library._configurations[configurationIdentifier] = configuration
			configuration.Library = library

		for contextIdentifier, context in document._contexts.items():
			if contextIdentifier in library._contexts:
				raise ContextExistsInLibraryError(context, library)

			library._contexts[contextIdentifier] = context
			context.Library = library

	def IterateDesignUnits(self, filter: DesignUnitKind = DesignUnitKind.All) -> Generator[DesignUnit, None, None]:
		for library in self._libraries.values():
			yield from library.IterateDesignUnits(filter)

	def Analyze(self) -> None:
		self.AnalyzeDependencies()
		self.AnalyzeObjects()

	def AnalyzeDependencies(self) -> None:
		self.CreateDependencyGraph()
		self.CreateCompileOrderGraph()

		self.IndexPackages()
		self.IndexArchitectures()

		self.LinkContexts()
		self.LinkArchitectures()
		self.LinkPackageBodies()
		self.LinkLibraryReferences()
		self.LinkPackageReferences()
		self.LinkContextReferences()

		self.LinkComponents()
		self.LinkInstantiations()
		self.CreateHierarchyGraph()
		self.ComputeCompileOrder()

	def AnalyzeObjects(self) -> None:
		self.IndexEntities()
		self.IndexPackageBodies()

		self.ImportObjects()
		self.CreateTypeAndObjectGraph()

	def CreateDependencyGraph(self) -> None:
		predefinedLibraries = ("std", "ieee")

		for libraryIdentifier, library in self._libraries.items():
			dependencyVertex = Vertex(vertexID=f"{libraryIdentifier}", value=library, graph=self._dependencyGraph)
			dependencyVertex["kind"] = DependencyGraphVertexKind.Library
			dependencyVertex["predefined"] = libraryIdentifier in predefinedLibraries
			library._dependencyVertex = dependencyVertex

			for contextIdentifier, context in library._contexts.items():
				dependencyVertex = Vertex(vertexID=f"{libraryIdentifier}.{contextIdentifier}", value=context, graph=self._dependencyGraph)
				dependencyVertex["kind"] = DependencyGraphVertexKind.Context
				dependencyVertex["predefined"] = context._library._normalizedIdentifier in predefinedLibraries
				context._dependencyVertex = dependencyVertex

			for packageIdentifier, package in library._packages.items():
				dependencyVertex = Vertex(vertexID=f"{libraryIdentifier}.{packageIdentifier}", value=package, graph=self._dependencyGraph)
				dependencyVertex["kind"] = DependencyGraphVertexKind.Package
				dependencyVertex["predefined"] = package._library._normalizedIdentifier in predefinedLibraries
				package._dependencyVertex = dependencyVertex

			for packageBodyIdentifier, packageBody in library._packageBodies.items():
				dependencyVertex = Vertex(vertexID=f"{libraryIdentifier}.{packageBodyIdentifier}(body)", value=packageBody, graph=self._dependencyGraph)
				dependencyVertex["kind"] = DependencyGraphVertexKind.PackageBody
				dependencyVertex["predefined"] = packageBody._library._normalizedIdentifier in predefinedLibraries
				packageBody._dependencyVertex = dependencyVertex

			for entityIdentifier, entity in library._entities.items():
				dependencyVertex = Vertex(vertexID=f"{libraryIdentifier}.{entityIdentifier}", value=entity, graph=self._dependencyGraph)
				dependencyVertex["kind"] = DependencyGraphVertexKind.Entity
				dependencyVertex["predefined"] = entity._library._normalizedIdentifier in predefinedLibraries
				entity._dependencyVertex = dependencyVertex

			for entityIdentifier, architectures in library._architectures.items():
				for architectureIdentifier, architecture in architectures.items():
					dependencyVertex = Vertex(vertexID=f"{libraryIdentifier}.{entityIdentifier}({architectureIdentifier})", value=architecture, graph=self._dependencyGraph)
					dependencyVertex["kind"] = DependencyGraphVertexKind.Architecture
					dependencyVertex["predefined"] = architecture._library._normalizedIdentifier in predefinedLibraries
					architecture._dependencyVertex = dependencyVertex

			for configurationIdentifier, configuration in library._configurations.items():
				dependencyVertex = Vertex(vertexID=f"{libraryIdentifier}.{configurationIdentifier}", value=configuration, graph=self._dependencyGraph)
				dependencyVertex["kind"] = DependencyGraphVertexKind.Configuration
				dependencyVertex["predefined"] = configuration._library._normalizedIdentifier in predefinedLibraries
				configuration._dependencyVertex = dependencyVertex

	def CreateCompileOrderGraph(self) -> None:
		for document in self._documents:
			dependencyVertex = Vertex(vertexID=document.Path.name, value=document, graph=self._dependencyGraph)
			dependencyVertex["kind"] = DependencyGraphVertexKind.Document
			document._dependencyVertex = dependencyVertex

			compilerOrderVertex = dependencyVertex.Copy(self._compileOrderGraph, copyDict=True, linkingKeyToOriginalVertex="dependencyVertex", linkingKeyFromOriginalVertex="compileOrderVertex")
			document._compileOrderVertex = compilerOrderVertex

			for designUnit in document._designUnits:
				edge = dependencyVertex.EdgeFromVertex(designUnit._dependencyVertex)
				edge["kind"] = DependencyGraphEdgeKind.SourceFile

	def ImportObjects(self):
		def _ImportObjects(package: Package):
			for referencedLibrary in package._referencedPackages.values():
				for referencedPackage in referencedLibrary.values():
					for declaredItem in referencedPackage._declaredItems:
						package._namespace._elements[declaredItem._identifier] = declaredItem

		for libraryName in ("std", "ieee"):
			for package in self.GetLibrary(libraryName).IterateDesignUnits(filter=DesignUnitKind.Package):  # type: Package
				_ImportObjects(package)

		for document in self.IterateDocumentsInCompileOrder():
			for package in document.IterateDesignUnits(filter=DesignUnitKind.Package):  # type: Package
				_ImportObjects(package)

	def CreateTypeAndObjectGraph(self) -> None:
		def _HandlePackage(package):
			packagePrefix = f"{package.Library.NormalizedIdentifier}.{package.NormalizedIdentifier}"

			for deferredConstant in package._deferredConstants.values():
				print(f"Deferred Constant: {deferredConstant}")
				deferredConstantVertex = Vertex(
					vertexID=f"{packagePrefix}.{deferredConstant.NormalizedIdentifiers[0]}",
					value=deferredConstant,
					graph=self._objectGraph
				)
				deferredConstantVertex["kind"] = ObjectGraphVertexKind.DeferredConstant
				deferredConstant._objectVertex = deferredConstantVertex

			for constant in package._constants.values():
				print(f"Constant: {constant}")
				constantVertex = Vertex(
					vertexID=f"{packagePrefix}.{constant.NormalizedIdentifiers[0]}",
					value=constant,
					graph=self._objectGraph
				)
				constantVertex["kind"] = ObjectGraphVertexKind.Constant
				constant._objectVertex = constantVertex

			for type in package._types.values():
				print(f"Type: {type}")
				typeVertex = Vertex(
					vertexID=f"{packagePrefix}.{type.NormalizedIdentifier}",
					value=type,
					graph=self._objectGraph
				)
				typeVertex["kind"] = ObjectGraphVertexKind.Type
				type._objectVertex = typeVertex

			for subtype in package._subtypes.values():
				print(f"Subtype: {subtype}")
				subtypeVertex = Vertex(
					vertexID=f"{packagePrefix}.{subtype.NormalizedIdentifier}",
					value=subtype,
					graph=self._objectGraph
				)
				subtypeVertex["kind"] = ObjectGraphVertexKind.Subtype
				subtype._objectVertex = subtypeVertex

			for function in package._functions.values():
				print(f"Function: {function}")
				functionVertex = Vertex(
					vertexID=f"{packagePrefix}.{function.NormalizedIdentifier}",
					value=function,
					graph=self._objectGraph
				)
				functionVertex["kind"] = ObjectGraphVertexKind.Function
				function._objectVertex = functionVertex

			for procedure in package._procedures.values():
				print(f"Procedure: {procedure}")
				procedureVertex = Vertex(
					vertexID=f"{packagePrefix}.{procedure.NormalizedIdentifier}",
					value=procedure,
					graph=self._objectGraph
				)
				procedureVertex["kind"] = ObjectGraphVertexKind.Function
				procedure._objectVertex = procedureVertex

			for signal in package._signals.values():
				print(f"Signal: {signal}")
				signalVertex = Vertex(
					vertexID=f"{packagePrefix}.{signal.NormalizedIdentifiers[0]}",
					value=signal,
					graph=self._objectGraph
				)
				signalVertex["kind"] = ObjectGraphVertexKind.Signal
				signal._objectVertex = signalVertex

		def _LinkSymbolsInExpression(expression, namespace: Namespace, typeVertex: Vertex):
			if isinstance(expression, UnaryExpression):
				_LinkSymbolsInExpression(expression.Operand, namespace, typeVertex)
			elif isinstance(expression, BinaryExpression):
				_LinkSymbolsInExpression(expression.LeftOperand, namespace, typeVertex)
				_LinkSymbolsInExpression(expression.RightOperand, namespace, typeVertex)
			elif isinstance(expression, TernaryExpression):
				pass
			elif isinstance(expression, SimpleObjectOrFunctionCallSymbol):
				obj = namespace.FindObject(expression)
				expression._reference = obj

				edge = obj._objectVertex.EdgeToVertex(typeVertex)
				edge["kind"] = ObjectGraphEdgeKind.ReferenceInExpression
			else:
				pass

		def _LinkItems(package: Package):
			for item in package._declaredItems:
				if isinstance(item, Constant):
					print(f"constant: {item}")
				elif isinstance(item, DeferredConstant):
					print(f"deferred constant: {item}")
				elif isinstance(item, Signal):
					print(f"signal: {item}")
				elif isinstance(item, IntegerType):
					typeNode = item._objectVertex

					_LinkSymbolsInExpression(item.Range.LeftBound, package._namespace, typeNode)
					_LinkSymbolsInExpression(item.Range.RightBound, package._namespace, typeNode)
				# elif isinstance(item, FloatingType):
				# 	print(f"signal: {item}")
				elif isinstance(item, PhysicalType):
					typeNode = item._objectVertex

					_LinkSymbolsInExpression(item.Range.LeftBound, package._namespace, typeNode)
					_LinkSymbolsInExpression(item.Range.RightBound, package._namespace, typeNode)
				elif isinstance(item, ArrayType):
					# Resolve dimensions
					for dimension in item._dimensions:
						subtype = package._namespace.FindSubtype(dimension)
						dimension._reference = subtype

						edge = item._objectVertex.EdgeToVertex(subtype._objectVertex)
						edge["kind"] = ObjectGraphEdgeKind.Subtype

					# Resolve element subtype
					subtype = package._namespace.FindSubtype(item._elementType)
					item._elementType._reference = subtype

					edge = item._objectVertex.EdgeToVertex(subtype._objectVertex)
					edge["kind"] = ObjectGraphEdgeKind.Subtype
				elif isinstance(item, RecordType):
					print(f"record: {item}")
				else:
					print(f"not handled: {item}")


		for libraryName in ("std", "ieee"):
			for package in self.GetLibrary(libraryName).IterateDesignUnits(filter=DesignUnitKind.Package):  # type: Package
				_HandlePackage(package)
				_LinkItems(package)

		for document in self.IterateDocumentsInCompileOrder():
			for package in document.IterateDesignUnits(filter=DesignUnitKind.Package):  # type: Package
				_HandlePackage(package)
				_LinkItems(package)

	def LinkContexts(self) -> None:
		"""
		Resolves and links all items (library clauses, use clauses and nested context references) in contexts.

		It iterates all contexts in the design. Therefore, the library of the context is used as the working library. By
		default, the working library is implicitly referenced in :data:`_referencedLibraries`. In addition, a new empty
		dictionary is created in :data:`_referencedPackages` and :data:`_referencedContexts` for that working library.

		At first, all library clauses are resolved (a library clause my have multiple library reference symbols). For each
		referenced library an entry in :data:`_referencedLibraries` is generated and new empty dictionaries in
		:data:`_referencedPackages` and :data:`_referencedContexts` for that working library. In addition, a vertex in the
		dependency graph is added for that relationship.

		At second, all use clauses are resolved (a use clause my have multiple package member reference symbols). For each
		references package,
		"""
		for context in self.IterateDesignUnits(DesignUnitKind.Context):  # type: Context
			# Create entries in _referenced*** for the current working library under its real name.
			workingLibrary: Library = context.Library
			libraryNormalizedIdentifier = workingLibrary._normalizedIdentifier

			context._referencedLibraries[libraryNormalizedIdentifier] = self._libraries[libraryNormalizedIdentifier]
			context._referencedPackages[libraryNormalizedIdentifier] = {}
			context._referencedContexts[libraryNormalizedIdentifier] = {}

			# Process all library clauses
			for libraryReference in context._libraryReferences:
				# A library clause can have multiple comma-separated references
				for libraryName in libraryReference.Symbols:
					libraryNormalizedIdentifier = libraryName.Name._normalizedIdentifier
					try:
						library = self._libraries[libraryNormalizedIdentifier]
					except KeyError:
						raise ReferencedLibraryNotExistingError(context, libraryName)
						# TODO: add position to these messages

					libraryName.Library = library

					context._referencedLibraries[libraryNormalizedIdentifier] = library
					context._referencedPackages[libraryNormalizedIdentifier] = {}
					context._referencedContexts[libraryNormalizedIdentifier] = {}
					# TODO: warn duplicate library reference

					dependency = context._dependencyVertex.EdgeToVertex(library._dependencyVertex, edgeValue=libraryReference)
					dependency["kind"] = DependencyGraphEdgeKind.LibraryClause

			# Process all use clauses
			for packageReference in context.PackageReferences:
				# A use clause can have multiple comma-separated references
				for symbol in packageReference.Symbols:  # type: PackageReferenceSymbol
					packageName = symbol.Name.Prefix
					libraryName = packageName.Prefix

					libraryNormalizedIdentifier = libraryName._normalizedIdentifier
					packageNormalizedIdentifier = packageName._normalizedIdentifier

					# In case work is used, resolve to the real library name.
					if libraryNormalizedIdentifier == "work":
						library: Library = context._library
						libraryNormalizedIdentifier = library._normalizedIdentifier
					elif libraryNormalizedIdentifier not in context._referencedLibraries:
						# TODO: This check doesn't trigger if it's the working library.
						raise VHDLModelException(f"Use clause references library '{libraryName._identifier}', which was not referenced by a library clause.")
					else:
						library = self._libraries[libraryNormalizedIdentifier]

					try:
						package = library._packages[packageNormalizedIdentifier]
					except KeyError:
						raise VHDLModelException(f"Package '{packageName._identifier}' not found in {'working ' if libraryName._normalizedIdentifier == 'work' else ''}library '{library._identifier}'.")

					symbol.Package = package

					# TODO: warn duplicate package reference
					context._referencedPackages[libraryNormalizedIdentifier][packageNormalizedIdentifier] = package

					dependency = context._dependencyVertex.EdgeToVertex(package._dependencyVertex, edgeValue=packageReference)
					dependency["kind"] = DependencyGraphEdgeKind.UseClause

					# TODO: update the namespace with visible members
					if isinstance(symbol, AllPackageMembersReferenceSymbol):
						pass

					elif isinstance(symbol, PackageMemberReferenceSymbol):
						raise NotImplementedError()
					else:
						raise VHDLModelException()

	def LinkArchitectures(self) -> None:
		for library in self._libraries.values():
			library.LinkArchitectures()

	def LinkPackageBodies(self) -> None:
		for library in self._libraries.values():
			library.LinkPackageBodies()

	def LinkLibraryReferences(self) -> None:
		DEFAULT_LIBRARIES = ("std",)

		for designUnit in self.IterateDesignUnits(DesignUnitKind.WithContext):
			# All primary units supporting a context, have at least one library implicitly referenced
			if isinstance(designUnit, PrimaryUnit):
				for libraryIdentifier in DEFAULT_LIBRARIES:
					referencedLibrary = self._libraries[libraryIdentifier]
					designUnit._referencedLibraries[libraryIdentifier] = referencedLibrary
					designUnit._referencedPackages[libraryIdentifier] = {}
					designUnit._referencedContexts[libraryIdentifier] = {}
					# TODO: catch KeyError on self._libraries[libName]
					# TODO: warn duplicate library reference

					dependency = designUnit._dependencyVertex.EdgeToVertex(referencedLibrary._dependencyVertex)
					dependency["kind"] = DependencyGraphEdgeKind.LibraryClause

				workingLibrary: Library = designUnit.Library
				libraryIdentifier = workingLibrary.NormalizedIdentifier
				referencedLibrary = self._libraries[libraryIdentifier]


				designUnit._referencedLibraries[libraryIdentifier] = referencedLibrary
				designUnit._referencedPackages[libraryIdentifier] = {}
				designUnit._referencedContexts[libraryIdentifier] = {}

				dependency = designUnit._dependencyVertex.EdgeToVertex(referencedLibrary._dependencyVertex)
				dependency["kind"] = DependencyGraphEdgeKind.LibraryClause

			# All secondary units inherit referenced libraries from their primary units.
			else:
				if isinstance(designUnit, Architecture):
					referencedLibraries = designUnit.Entity.Entity._referencedLibraries
				elif isinstance(designUnit, PackageBody):
					referencedLibraries = designUnit.Package.Package._referencedLibraries
				else:
					raise VHDLModelException()

				for libraryIdentifier, library in referencedLibraries.items():
					designUnit._referencedLibraries[libraryIdentifier] = library

			for libraryReference in designUnit._libraryReferences:
				# A library clause can have multiple comma-separated references
				for librarySymbol in libraryReference.Symbols:
					libraryIdentifier = librarySymbol.Name.NormalizedIdentifier
					try:
						library = self._libraries[libraryIdentifier]
					except KeyError:
						ex = VHDLModelException(f"Library '{librarySymbol.Name.Identifier}' referenced by library clause of design unit '{designUnit.Identifier}' doesn't exist in design.")
						ex.add_note(f"""Known libraries: '{"', '".join(library for library in self._libraries)}'""")
						raise ex

					librarySymbol.Library = library
					designUnit._referencedLibraries[libraryIdentifier] = library
					designUnit._referencedPackages[libraryIdentifier] = {}
					designUnit._referencedContexts[libraryIdentifier] = {}
					# TODO: warn duplicate library reference

					dependency = designUnit._dependencyVertex.EdgeToVertex(library._dependencyVertex, edgeValue=libraryReference)
					dependency["kind"] = DependencyGraphEdgeKind.LibraryClause

	def LinkPackageReferences(self) -> None:
		DEFAULT_PACKAGES = (
			("std", ("standard",)),
		)

		for designUnit in self.IterateDesignUnits(DesignUnitKind.WithContext):
			# All primary units supporting a context, have at least one package implicitly referenced
			if isinstance(designUnit, PrimaryUnit):
				if designUnit.Library.NormalizedIdentifier != "std" and \
					designUnit.NormalizedIdentifier != "standard":
					for lib in DEFAULT_PACKAGES:
						if lib[0] not in designUnit._referencedLibraries:
							raise VHDLModelException()
						for pack in lib[1]:
							referencedPackage = self._libraries[lib[0]]._packages[pack]
							designUnit._referencedPackages[lib[0]][pack] = referencedPackage
							# TODO: catch KeyError on self._libraries[lib[0]]._packages[pack]
							# TODO: warn duplicate package reference

							dependency = designUnit._dependencyVertex.EdgeToVertex(referencedPackage._dependencyVertex)
							dependency["kind"] = DependencyGraphEdgeKind.UseClause


			# All secondary units inherit referenced packages from their primary units.
			else:
				if isinstance(designUnit, Architecture):
					referencedPackages = designUnit.Entity.Entity._referencedPackages
				elif isinstance(designUnit, PackageBody):
					referencedPackages = designUnit.Package.Package._referencedPackages
				else:
					raise VHDLModelException()

				for packageIdentifier, package in referencedPackages.items():
					designUnit._referencedPackages[packageIdentifier] = package

			for packageReference in designUnit.PackageReferences:
				# A use clause can have multiple comma-separated references
				for packageMemberSymbol in packageReference.Symbols:
					packageName = packageMemberSymbol.Name.Prefix
					libraryName = packageName.Prefix

					libraryIdentifier = libraryName.NormalizedIdentifier
					packageIdentifier = packageName.NormalizedIdentifier

					# In case work is used, resolve to the real library name.
					if libraryIdentifier == "work":
						library: Library = designUnit.Library
						libraryIdentifier = library.NormalizedIdentifier
					elif libraryIdentifier not in designUnit._referencedLibraries:
						# TODO: This check doesn't trigger if it's the working library.
						raise VHDLModelException(f"Use clause references library '{libraryName.Identifier}', which was not referenced by a library clause.")
					else:
						library = self._libraries[libraryIdentifier]

					try:
						package = library._packages[packageIdentifier]
					except KeyError:
						ex = VHDLModelException(f"Package '{packageName.Identifier}' not found in {'working ' if libraryName.NormalizedIdentifier == 'work' else ''}library '{library.Identifier}'.")
						ex.add_note(f"Caused in design unit '{designUnit}' in file '{designUnit.Document}'.")
						raise ex

					packageMemberSymbol.Package = package

					# TODO: warn duplicate package reference
					designUnit._referencedPackages[libraryIdentifier][packageIdentifier] = package

					dependency = designUnit._dependencyVertex.EdgeToVertex(package._dependencyVertex, edgeValue=packageReference)
					dependency["kind"] = DependencyGraphEdgeKind.UseClause

					# TODO: update the namespace with visible members
					if isinstance(packageMemberSymbol, AllPackageMembersReferenceSymbol):
						for componentIdentifier, component in package._components.items():
							designUnit._namespace._elements[componentIdentifier] = component

					elif isinstance(packageMemberSymbol, PackageMemberReferenceSymbol):
						raise NotImplementedError()
					else:
						raise VHDLModelException()

	def LinkContextReferences(self) -> None:
		for designUnit in self.IterateDesignUnits():
			for contextReference in designUnit._contextReferences:
				# A context reference can have multiple comma-separated references
				for contextSymbol in contextReference.Symbols:
					libraryName = contextSymbol.Name.Prefix

					libraryIdentifier = libraryName.NormalizedIdentifier
					contextIdentifier = contextSymbol.Name.NormalizedIdentifier

					# In case work is used, resolve to the real library name.
					if libraryIdentifier == "work":
						referencedLibrary = designUnit.Library
						libraryIdentifier = referencedLibrary.NormalizedIdentifier
					elif libraryIdentifier not in designUnit._referencedLibraries:
						# TODO: This check doesn't trigger if it's the working library.
						raise VHDLModelException(f"Context reference references library '{libraryName.Identifier}', which was not referenced by a library clause.")
					else:
						referencedLibrary = self._libraries[libraryIdentifier]

					try:
						referencedContext = referencedLibrary._contexts[contextIdentifier]
					except KeyError:
						raise VHDLModelException(f"Context '{contextSymbol.Name.Identifier}' not found in {'working ' if libraryName.NormalizedIdentifier == 'work' else ''}library '{referencedLibrary.Identifier}'.")

					contextSymbol.Package = referencedContext

					# TODO: warn duplicate referencedContext reference
					designUnit._referencedContexts[libraryIdentifier][contextIdentifier] = referencedContext

					dependency = designUnit._dependencyVertex.EdgeToVertex(referencedContext._dependencyVertex, edgeValue=contextReference)
					dependency["kind"] = DependencyGraphEdgeKind.ContextReference

		for vertex in self._dependencyGraph.IterateTopologically():
			if vertex["kind"] is DependencyGraphVertexKind.Context:
				context: Context = vertex.Value
				for designUnitVertex in vertex.IteratePredecessorVertices():
					designUnit: DesignUnit = designUnitVertex.Value
					for libraryIdentifier, library in context._referencedLibraries.items():
						# if libraryIdentifier in designUnit._referencedLibraries:
						# 	raise VHDLModelException(f"Referenced library '{library.Identifier}' already exists in references for design unit '{designUnit.Identifier}'.")

						designUnit._referencedLibraries[libraryIdentifier] = library
						designUnit._referencedPackages[libraryIdentifier] = {}

					for libraryIdentifier, packages in context._referencedPackages.items():
						for packageIdentifier, package in packages.items():
							if packageIdentifier in designUnit._referencedPackages:
								raise VHDLModelException(f"Referenced package '{package.Identifier}' already exists in references for design unit '{designUnit.Identifier}'.")

							designUnit._referencedPackages[libraryIdentifier][packageIdentifier] = package

	def LinkComponents(self) -> None:
		for package in self.IterateDesignUnits(DesignUnitKind.Package):  # type: Package
			library = package._library
			for component in package._components.values():
				try:
					entity = library._entities[component.NormalizedIdentifier]
				except KeyError:
					print(f"Entity '{component.Identifier}' not found for component '{component.Identifier}' in library '{library.Identifier}'.")

				component.Entity = entity

				# QUESTION: Add link in dependency graph as dashed line from component to entity?
				#           Currently, component has no _dependencyVertex field

	def LinkInstantiations(self) -> None:
		for architecture in self.IterateDesignUnits(DesignUnitKind.Architecture):  # type: Architecture
			for instance in architecture.IterateInstantiations():
				if isinstance(instance, EntityInstantiation):
					libraryName = instance.Entity.Name.Prefix
					libraryIdentifier = libraryName.Identifier
					normalizedLibraryIdentifier = libraryName.NormalizedIdentifier
					if normalizedLibraryIdentifier == "work":
						libraryIdentifier = architecture.Library.Identifier
						normalizedLibraryIdentifier = architecture.Library.NormalizedIdentifier
					elif normalizedLibraryIdentifier not in architecture._referencedLibraries:
						ex = VHDLModelException(f"Referenced library '{libraryIdentifier}' in direct entity instantiation '{instance.Label}: entity {instance.Entity.Prefix.Identifier}.{instance.Entity.Identifier}' not found in architecture '{architecture!r}'.")
						ex.add_note(f"Add a library reference to the architecture or entity using a library clause like: 'library {libraryIdentifier};'.")
						raise ex

					try:
						library = self._libraries[normalizedLibraryIdentifier]
					except KeyError:
						ex = VHDLModelException(f"Referenced library '{libraryIdentifier}' in direct entity instantiation '{instance.Label}: entity {instance.Entity.Prefix.Identifier}.{instance.Entity.Identifier}' not found in design.")
						ex.add_note(f"No design units were parsed into library '{libraryIdentifier}'. Thus it doesn't exist in design.")
						raise ex

					try:
						entity = library._entities[instance.Entity.Name.NormalizedIdentifier]
					except KeyError:
						ex = VHDLModelException(f"Referenced entity '{instance.Entity.Name.Identifier}' in direct entity instantiation '{instance.Label}: entity {instance.Entity.Name.Prefix.Identifier}.{instance.Entity.Name.Identifier}' not found in {'working ' if instance.Entity.Name.Prefix.NormalizedIdentifier == 'work' else ''}library '{libraryIdentifier}'.")
						libs = [library.Identifier for library in self._libraries.values() for entityIdentifier in library._entities.keys() if entityIdentifier == instance.Entity.Name.NormalizedIdentifier]
						if libs:
							ex.add_note(f"Found entity '{instance.Entity!s}' in other libraries: {', '.join(libs)}")
						raise ex

					instance.Entity.Entity = entity

					dependency = architecture._dependencyVertex.EdgeToVertex(entity._dependencyVertex, edgeValue=instance)
					dependency["kind"] = DependencyGraphEdgeKind.EntityInstantiation

				elif isinstance(instance, ComponentInstantiation):
					component = architecture._namespace.FindComponent(instance.Component)

					instance.Component.Component = component

					dependency = architecture._dependencyVertex.EdgeToVertex(component.Entity._dependencyVertex, edgeValue=instance)
					dependency["kind"] = DependencyGraphEdgeKind.ComponentInstantiation

				elif isinstance(instance, ConfigurationInstantiation):
					# pass
					print(instance.Label, instance.Configuration)

	def IndexPackages(self) -> None:
		for library in self._libraries.values():
			library.IndexPackages()

	def IndexPackageBodies(self) -> None:
		for library in self._libraries.values():
			library.IndexPackageBodies()

	def IndexEntities(self) -> None:
		for library in self._libraries.values():
			library.IndexEntities()

	def IndexArchitectures(self) -> None:
		for library in self._libraries.values():
			library.IndexArchitectures()

	def CreateHierarchyGraph(self) -> None:
		# Copy all entity and architecture vertices from dependency graph to hierarchy graph and double-link them
		entityArchitectureFilter = lambda v: v["kind"] in DependencyGraphVertexKind.Entity | DependencyGraphVertexKind.Architecture
		for vertex in self._dependencyGraph.IterateVertices(predicate=entityArchitectureFilter):
			hierarchyVertex = vertex.Copy(self._hierarchyGraph, copyDict=True, linkingKeyToOriginalVertex="dependencyVertex", linkingKeyFromOriginalVertex="hierarchyVertex")
			vertex.Value._hierarchyVertex = hierarchyVertex

		# Copy implementation edges from
		for hierarchyArchitectureVertex in self._hierarchyGraph.IterateVertices(predicate=lambda v: v["kind"] is DependencyGraphVertexKind.Architecture):
			for dependencyEdge in hierarchyArchitectureVertex["dependencyVertex"].IterateOutboundEdges():
				kind: DependencyGraphEdgeKind = dependencyEdge["kind"]
				if DependencyGraphEdgeKind.Implementation in kind:
					hierarchyDestinationVertex = dependencyEdge.Destination["hierarchyVertex"]
					newEdge = hierarchyArchitectureVertex.EdgeFromVertex(hierarchyDestinationVertex)
				elif DependencyGraphEdgeKind.Instantiation in kind:
					hierarchyDestinationVertex = dependencyEdge.Destination["hierarchyVertex"]

					# FIXME: avoid parallel edges, to graph can be converted to a tree until "real" hierarchy is computed (unrole generics and blocks)
					if hierarchyArchitectureVertex.HasEdgeToDestination(hierarchyDestinationVertex):
						continue

					newEdge = hierarchyArchitectureVertex.EdgeToVertex(hierarchyDestinationVertex)
				else:
					continue

				newEdge["kind"] = kind

	def ComputeCompileOrder(self) -> None:
		def predicate(edge: Edge) -> bool:
			return (
				DependencyGraphEdgeKind.Implementation in edge["kind"] or
				DependencyGraphEdgeKind.Instantiation in edge["kind"] or
				DependencyGraphEdgeKind.UseClause in edge["kind"] or
				DependencyGraphEdgeKind.ContextReference in edge["kind"]
			) and edge.Destination["predefined"] is False

		for edge in self._dependencyGraph.IterateEdges(predicate=predicate):
			sourceDocument:      Document = edge.Source.Value.Document
			destinationDocument: Document = edge.Destination.Value.Document

			sourceVertex =      sourceDocument._compileOrderVertex
			destinationVertex = destinationDocument._compileOrderVertex

			# Don't add self-edges
			if sourceVertex is destinationVertex:
				continue
			# Don't add parallel edges
			elif sourceVertex.HasEdgeToDestination(destinationVertex):
				continue

			e = sourceVertex.EdgeToVertex(destinationVertex)
			e["kind"] = DependencyGraphEdgeKind.CompileOrder

			e = sourceVertex["dependencyVertex"].EdgeToVertex(destinationVertex["dependencyVertex"])
			e["kind"] = DependencyGraphEdgeKind.CompileOrder

	def IterateDocumentsInCompileOrder(self) -> Generator['Document', None, None]:
		if self._compileOrderGraph.EdgeCount < self._compileOrderGraph.VertexCount - 1:
			raise VHDLModelException(f"Compile order is not yet computed from dependency graph.")

		for compileOrderNode in self._compileOrderGraph.IterateTopologically():
			yield compileOrderNode.Value

	def GetUnusedDesignUnits(self) -> List[DesignUnit]:
		raise NotImplementedError()

	def __repr__(self) -> str:
		return f"Design: {self._name}"

	__str__ = __repr__


@export
class Library(ModelEntity, NamedEntityMixin):
	"""A ``Library`` represents a VHDL library. It contains all *primary* and *secondary* design units."""

	_contexts:       Dict[str, Context]                  #: Dictionary of all contexts defined in a library.
	_configurations: Dict[str, Configuration]            #: Dictionary of all configurations defined in a library.
	_entities:       Dict[str, Entity]                   #: Dictionary of all entities defined in a library.
	_architectures:  Dict[str, Dict[str, Architecture]]  #: Dictionary of all architectures defined in a library.
	_packages:       Dict[str, Package]                  #: Dictionary of all packages defined in a library.
	_packageBodies:  Dict[str, PackageBody]              #: Dictionary of all package bodies defined in a library.

	_dependencyVertex: Vertex[None, None, str, Union['Library', DesignUnit], None, None, None, None, None, None, None, None, None, None, None, None, None]

	def __init__(self, identifier: str):
		super().__init__()
		NamedEntityMixin.__init__(self, identifier)

		self._contexts =        {}
		self._configurations =  {}
		self._entities =        {}
		self._architectures =   {}
		self._packages =        {}
		self._packageBodies =   {}

		self._dependencyVertex = None

	@property
	def Contexts(self) -> Dict[str, Context]:
		"""Returns a list of all context declarations declared in this library."""
		return self._contexts

	@property
	def Configurations(self) -> Dict[str, Configuration]:
		"""Returns a list of all configuration declarations declared in this library."""
		return self._configurations

	@property
	def Entities(self) -> Dict[str, Entity]:
		"""Returns a list of all entity declarations declared in this library."""
		return self._entities

	@property
	def Architectures(self) -> Dict[str, Dict[str, Architecture]]:
		"""Returns a list of all architectures declarations declared in this library."""
		return self._architectures

	@property
	def Packages(self) -> Dict[str, Package]:
		"""Returns a list of all package declarations declared in this library."""
		return self._packages

	@property
	def PackageBodies(self) -> Dict[str, PackageBody]:
		"""Returns a list of all package body declarations declared in this library."""
		return self._packageBodies

	@property
	def DependencyVertex(self) -> Vertex:
		return self._dependencyVertex

	def IterateDesignUnits(self, filter: DesignUnitKind = DesignUnitKind.All) -> Generator[DesignUnit, None, None]:
		if DesignUnitKind.Context in filter:
			for context in self._contexts.values():
				yield context

		if DesignUnitKind.Package in filter:
			for package in self._packages.values():
				yield package

		if DesignUnitKind.PackageBody in filter:
			for packageBody in self._packageBodies.values():
				yield packageBody

		if DesignUnitKind.Entity in filter:
			for entity in self._entities.values():
				yield entity

		if DesignUnitKind.Architecture in filter:
			for architectures in self._architectures.values():
				for architecture in architectures.values():
					yield architecture

		if DesignUnitKind.Configuration in filter:
			for configuration in self._configurations.values():
				yield configuration

		# for verificationProperty in self._verificationUnits.values():
		# 	yield verificationProperty
		# for verificationUnit in self._verificationProperties.values():
		# 	yield entity
		# for verificationMode in self._verificationModes.values():
		# 	yield verificationMode

	def LinkArchitectures(self):
		for entityName, architecturesPerEntity in self._architectures.items():
			if entityName not in self._entities:
				architectureNames = "', '".join(architecturesPerEntity.keys())
				raise VHDLModelException(f"Entity '{entityName}' referenced by architecture(s) '{architectureNames}' doesn't exist in library '{self._identifier}'.")
				# TODO: search in other libraries to find that entity.
				# TODO: add code position

			for architecture in architecturesPerEntity.values():
				entity = self._entities[entityName]

				if architecture.NormalizedIdentifier in entity._architectures:
					raise VHDLModelException(f"Architecture '{architecture._identifier}' already exists for entity '{entity._identifier}'.")
					# TODO: add code position of existing and current

				entity._architectures[architecture.NormalizedIdentifier] = architecture
				architecture._entity.Entity = entity
				architecture._namespace.ParentNamespace = entity._namespace

				# add "architecture -> entity" relation in dependency graph
				dependency = architecture._dependencyVertex.EdgeToVertex(entity._dependencyVertex)
				dependency["kind"] = DependencyGraphEdgeKind.EntityImplementation

	def LinkPackageBodies(self):
		for packageBodyName, packageBody in self._packageBodies.items():
			if packageBodyName not in self._packages:
				raise VHDLModelException(f"Package '{packageBodyName}' referenced by package body '{packageBodyName}' doesn't exist in library '{self._identifier}'.")

			package = self._packages[packageBodyName]
			packageBody._package.Package = package
			packageBody._namespace.ParentNamespace = package._namespace

			# add "package body -> package" relation in dependency graph
			dependency = packageBody._dependencyVertex.EdgeToVertex(package._dependencyVertex)
			dependency["kind"] = DependencyGraphEdgeKind.PackageImplementation

	def IndexPackages(self):
		for package in self._packages.values():
			if isinstance(package, Package):
				package.IndexDeclaredItems()

	def IndexPackageBodies(self):
		for packageBody in self._packageBodies.values():
			packageBody.IndexDeclaredItems()

	def IndexEntities(self):
		for entity in self._entities.values():
			entity.IndexDeclaredItems()

	def IndexArchitectures(self):
		for architectures in self._architectures.values():
			for architecture in architectures.values():
				architecture.IndexDeclaredItems()
				architecture.IndexStatements()

	def __repr__(self) -> str:
		return f"Library: '{self._identifier}'"

	__str__ = __repr__


@export
class Document(ModelEntity, DocumentedEntityMixin):
	"""A ``Document`` represents a sourcefile. It contains *primary* and *secondary* design units."""

	_path:                   Path                                  #: path to the document. ``None`` if virtual document.
	_designUnits:            List[DesignUnit]                    #: List of all design units defined in a document.
	_contexts:               Dict[str, Context]                  #: Dictionary of all contexts defined in a document.
	_configurations:         Dict[str, Configuration]            #: Dictionary of all configurations defined in a document.
	_entities:               Dict[str, Entity]                   #: Dictionary of all entities defined in a document.
	_architectures:          Dict[str, Dict[str, Architecture]]  #: Dictionary of all architectures defined in a document.
	_packages:               Dict[str, Package]                  #: Dictionary of all packages defined in a document.
	_packageBodies:          Dict[str, PackageBody]              #: Dictionary of all package bodies defined in a document.
	_verificationUnits:      Dict[str, VerificationUnit]         #: Dictionary of all PSL verification units defined in a document.
	_verificationProperties: Dict[str, VerificationProperty]     #: Dictionary of all PSL verification properties defined in a document.
	_verificationModes:      Dict[str, VerificationMode]         #: Dictionary of all PSL verification modes defined in a document.

	_dependencyVertex:       Vertex[None, None, None, 'Document', None, None, None, None, None, None, None, None, None, None, None, None, None]
	_compileOrderVertex:     Vertex[None, None, None, 'Document', None, None, None, None, None, None, None, None, None, None, None, None, None]

	def __init__(self, path: Path, documentation: str = None):
		super().__init__()
		DocumentedEntityMixin.__init__(self, documentation)

		self._path =                   path
		self._designUnits =            []
		self._contexts =               {}
		self._configurations =         {}
		self._entities =               {}
		self._architectures =          {}
		self._packages =               {}
		self._packageBodies =          {}
		self._verificationUnits =      {}
		self._verificationProperties = {}
		self._verificationModes =      {}

		self._dependencyVertex = None
		self._compileOrderVertex = None

	def _AddEntity(self, item: Entity) -> None:
		if not isinstance(item, Entity):
			raise TypeError(f"Parameter 'item' is not of type 'Entity'.")

		identifier = item.NormalizedIdentifier
		if identifier in self._entities:
			raise ValueError(f"An entity '{item.Identifier}' already exists in this document.")

		self._entities[identifier] = item
		self._designUnits.append(item)
		item._parent = self


	def _AddArchitecture(self, item: Architecture) -> None:
		if not isinstance(item, Architecture):
			raise TypeError(f"Parameter 'item' is not of type 'Architecture'.")

		entity = item.Entity.Name
		entityIdentifier = entity.NormalizedIdentifier
		try:
			architectures = self._architectures[entityIdentifier]
			if item.Identifier in architectures:
				raise ValueError(f"An architecture '{item.Identifier}' for entity '{entity.Identifier}' already exists in this document.")

			architectures[item.Identifier] = item
		except KeyError:
			self._architectures[entityIdentifier] = {item.Identifier: item}

		self._designUnits.append(item)
		item._parent = self

	def _AddPackage(self, item: Package) -> None:
		if not isinstance(item, (Package, PackageInstantiation)):
			raise TypeError(f"Parameter 'item' is not of type 'Package' or 'PackageInstantiation'.")

		identifier = item.NormalizedIdentifier
		if identifier in self._packages:
			raise ValueError(f"A package '{item.Identifier}' already exists in this document.")

		self._packages[identifier] = item
		self._designUnits.append(item)
		item._parent = self

	def _AddPackageBody(self, item: PackageBody) -> None:
		if not isinstance(item, PackageBody):
			raise TypeError(f"Parameter 'item' is not of type 'PackageBody'.")

		identifier = item.NormalizedIdentifier
		if identifier in self._packageBodies:
			raise ValueError(f"A package body '{item.Identifier}' already exists in this document.")

		self._packageBodies[identifier] = item
		self._designUnits.append(item)
		item._parent = self

	def _AddContext(self, item: Context) -> None:
		if not isinstance(item, Context):
			raise TypeError(f"Parameter 'item' is not of type 'Context'.")

		identifier = item.NormalizedIdentifier
		if identifier in self._contexts:
			raise ValueError(f"A context '{item.Identifier}' already exists in this document.")

		self._contexts[identifier] = item
		self._designUnits.append(item)
		item._parent = self

	def _AddConfiguration(self, item: Configuration) -> None:
		if not isinstance(item, Configuration):
			raise TypeError(f"Parameter 'item' is not of type 'Configuration'.")

		identifier = item.NormalizedIdentifier
		if identifier in self._configurations:
			raise ValueError(f"A configuration '{item.Identifier}' already exists in this document.")

		self._configurations[identifier] = item
		self._designUnits.append(item)
		item._parent = self

	def _AddVerificationUnit(self, item: VerificationUnit) -> None:
		if not isinstance(item, VerificationUnit):
			raise TypeError(f"Parameter 'item' is not of type 'VerificationUnit'.")

		identifier = item.NormalizedIdentifier
		if identifier in self._verificationUnits:
			raise ValueError(f"A verification unit '{item.Identifier}' already exists in this document.")

		self._verificationUnits[identifier] = item
		self._designUnits.append(item)
		item._parent = self

	def _AddVerificationProperty(self, item: VerificationProperty) -> None:
		if not isinstance(item, VerificationProperty):
			raise TypeError(f"Parameter 'item' is not of type 'VerificationProperty'.")

		identifier = item.NormalizedIdentifier
		if identifier in self._verificationProperties:
			raise ValueError(f"A verification property '{item.Identifier}' already exists in this document.")

		self._verificationProperties[identifier] = item
		self._designUnits.append(item)
		item._parent = self

	def _AddVerificationMode(self, item: VerificationMode) -> None:
		if not isinstance(item, VerificationMode):
			raise TypeError(f"Parameter 'item' is not of type 'VerificationMode'.")

		identifier = item.NormalizedIdentifier
		if identifier in self._verificationModes:
			raise ValueError(f"A verification mode '{item.Identifier}' already exists in this document.")

		self._verificationModes[identifier] = item
		self._designUnits.append(item)
		item._parent = self

	def _AddDesignUnit(self, item: DesignUnit) -> None:
		identifier = item.NormalizedIdentifier
		if isinstance(item, Entity):
			self._entities[identifier] = item
		elif isinstance(item, Architecture):
			entityIdentifier = item.Entity.Name.NormalizedIdentifier
			try:
				architectures = self._architectures[entityIdentifier]
				if identifier in architectures:
					raise ValueError(f"An architecture '{item.Identifier}' for entity '{item.Entity.Identifier}' already exists in this document.")

				architectures[identifier] = item
			except KeyError:
				self._architectures[entityIdentifier] = {identifier: item}
		elif isinstance(item, Package):
			self._packages[identifier] = item
		elif isinstance(item, PackageBody):
			self._packageBodies[identifier] = item
		elif isinstance(item, Context):
			self._contexts[identifier] = item
		elif isinstance(item, Configuration):
			self._configurations[identifier] = item
		elif isinstance(item, VerificationUnit):
			self._verificationUnits[identifier] = item
		elif isinstance(item, VerificationProperty):
			self._verificationProperties[identifier] = item
		elif isinstance(item, VerificationMode):
			self._verificationModes[identifier] = item
		elif isinstance(item, DesignUnit):
			raise TypeError(f"Parameter 'item' is an unknown 'DesignUnit'.")
		else:
			raise TypeError(f"Parameter 'item' is not of type 'DesignUnit'.")

		self._designUnits.append(item)
		item._parent = self

	@property
	def Path(self) -> Path:
		return self._path

	@property
	def DesignUnits(self) -> List[DesignUnit]:
		"""Returns a list of all design units declarations found in this document."""
		return self._designUnits

	@property
	def Contexts(self) -> Dict[str, Context]:
		"""Returns a list of all context declarations found in this document."""
		return self._contexts

	@property
	def Configurations(self) -> Dict[str, Configuration]:
		"""Returns a list of all configuration declarations found in this document."""
		return self._configurations

	@property
	def Entities(self) -> Dict[str, Entity]:
		"""Returns a list of all entity declarations found in this document."""
		return self._entities

	@property
	def Architectures(self) -> Dict[str, Dict[str, Architecture]]:
		"""Returns a list of all architecture declarations found in this document."""
		return self._architectures

	@property
	def Packages(self) -> Dict[str, Package]:
		"""Returns a list of all package declarations found in this document."""
		return self._packages

	@property
	def PackageBodies(self) -> Dict[str, PackageBody]:
		"""Returns a list of all package body declarations found in this document."""
		return self._packageBodies

	@property
	def VerificationUnits(self) -> Dict[str, VerificationUnit]:
		"""Returns a list of all verification unit declarations found in this document."""
		return self._verificationUnits

	@property
	def VerificationProperties(self) -> Dict[str, VerificationProperty]:
		"""Returns a list of all verification property declarations found in this document."""
		return self._verificationProperties

	@property
	def VerificationModes(self) -> Dict[str, VerificationMode]:
		"""Returns a list of all verification mode declarations found in this document."""
		return self._verificationModes

	@property
	def CompileOrderVertex(self) -> Vertex[None, None, None, 'Document', None, None, None, None, None, None, None, None, None, None, None, None, None]:
		return self._compileOrderVertex

	def IterateDesignUnits(self, filter: DesignUnitKind = DesignUnitKind.All) -> Generator[DesignUnit, None, None]:
		if DesignUnitKind.Context in filter:
			for context in self._contexts.values():
				yield context

		if DesignUnitKind.Package in filter:
			for package in self._packages.values():
				yield package

		if DesignUnitKind.PackageBody in filter:
			for packageBody in self._packageBodies.values():
				yield packageBody

		if DesignUnitKind.Entity in filter:
			for entity in self._entities.values():
				yield entity

		if DesignUnitKind.Architecture in filter:
			for architectures in self._architectures.values():
				for architecture in architectures.values():
					yield architecture

		if DesignUnitKind.Configuration in filter:
			for configuration in self._configurations.values():
				yield configuration

		# for verificationProperty in self._verificationUnits.values():
		# 	yield verificationProperty
		# for verificationUnit in self._verificationProperties.values():
		# 	yield entity
		# for verificationMode in self._verificationModes.values():
		# 	yield verificationMode

	def __repr__(self) -> str:
		return f"Document: '{self._path}'"

	__str__ = __repr__
