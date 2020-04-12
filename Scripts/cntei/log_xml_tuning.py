import sims4.core_services
import sims4.log
from cntei.modinfo import ModInfo
from cntei.watcher import TuningWatcher
from sims4.tuning.merged_tuning_manager import get_manager, MergedTuningAttr, UnavailablePackSafeResourceError
from sims4.tuning.serialization import ETreeTuningLoader, _DeferredEtreeTunableLoader
from sims4.tuning.tunable import TunableTuple, TunableVariant, _TunableCollection
from sims4.tuning.tunable_base import LoadingAttributes, Tags
from sims4.tuning.tunable_errors import TunableMinimumLengthError
from xml.etree import ElementTree

from sims4communitylib.exceptions.common_exceptions_handler import CommonExceptionHandler
from sims4communitylib.utils.common_injection_utils import CommonInjectionUtils


class _CNTEIXMLValidator:
    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def _log_etree_node(xml_node):
        TuningWatcher.get().process_log_message('ETree Node:')
        xml_text = ElementTree.tostring(xml_node).decode()
        for line in xml_text.splitlines():
            TuningWatcher.get().process_log_message('  {}', line)

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def _serialization_load_tunable(original_self, tunable_class, tunable_name, tunable, cur_node, mtg):
        if cur_node.tag != MergedTuningAttr.Reference:
            current_tunable_tag = tunable.LOADING_TAG_NAME
            if current_tunable_tag == Tags.TdescFragTag:
                current_tunable_tag = tunable.FRAG_TAG_NAME
            if current_tunable_tag != cur_node.tag:
                TuningWatcher.get().process_log_message("Incorrectly matched tuning types found in tuning for {} in {}. Expected '{}', got '{}'", tunable_name, original_self.source, current_tunable_tag, cur_node.tag)
                TuningWatcher.get().process_log_message('ATTRS: {}', cur_node.items())
                _CNTEIXMLValidator._log_etree_node(cur_node)
        try:
            deferred = False
            if tunable.deferred and sims4.core_services.defer_tuning_references:
                value = _DeferredEtreeTunableLoader(tunable, node=cur_node, source=original_self.source)
                sims4.tuning.serialization._deferred_tuning_loaders.append(value)
                deferred = True
            elif cur_node.tag == MergedTuningAttr.Reference:
                ref_index = cur_node.get(MergedTuningAttr.Index)
                value = mtg.get_tunable(ref_index, tunable, original_self.source)
            else:
                value = tunable.load_etree_node(node=cur_node, source=original_self.source, expect_error=False)
            reload_context = getattr(tunable_class, '__reload_context__', None)
            if reload_context:
                with reload_context(tunable_class, tunable_class):
                    setattr(tunable_class, tunable_name, value)
            else:
                setattr(tunable_class, tunable_name, value)
            if not deferred:
                original_self._invoke_names.append(tunable_name)
        except Exception as ex:
            TuningWatcher.get().process_log_message("Error occurred within the tag named '{}' (value: {})", cur_node.get(LoadingAttributes.Name), cur_node.tag)
            raise ex

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def _tuple_load_etree_node(original_self, node, source, expect_error):
        value = {}
        tuned = set()
        mtg = get_manager()
        if node is not None:
            for child_node in node:
                name = child_node.get(LoadingAttributes.Name)
                if name in original_self.tunable_items:
                    template = original_self.tunable_items.get(name)
                    if child_node.tag == MergedTuningAttr.Reference:
                        ref_index = child_node.get(MergedTuningAttr.Index)
                        tuple_value = mtg.get_tunable(ref_index, template, source)
                    else:
                        current_tunable_tag = template.LOADING_TAG_NAME
                        if current_tunable_tag == Tags.TdescFragTag:
                            current_tunable_tag = template.FRAG_TAG_NAME
                        if current_tunable_tag != child_node.tag:
                            tunable_name = node.get(LoadingAttributes.Name, '<Unnamed>')
                            TuningWatcher.get().process_log_message("Incorrectly matched tuning types found in tuning for {} in {}. Expected '{}', got '{}'", tunable_name, source, current_tunable_tag, child_node.tag)
                            TuningWatcher.get().process_log_message('ATTRS 2: {}', node.items())
                            _CNTEIXMLValidator._log_etree_node(child_node)
                        tuple_value = template.load_etree_node(child_node, source, expect_error)
                    value[name] = tuple_value
                    tuned.add(name)
                else:
                    TuningWatcher.get().process_log_message('Error in {}, parsing a {} tag', source, original_self.TAGNAME)
                    if name in original_self.locked_args:
                        TuningWatcher.get().process_log_message("The tag name '{}' is locked for this tunable and should be removed from the tuning file.", name)
                    else:
                        TuningWatcher.get().process_log_message("The tag name '{}' was unexpected.  Valid tags: {}", name, ', '.join(original_self.tunable_items.keys()))
        if original_self.INCLUDE_UNTUNED_VALUES:
            leftovers = set(original_self.tunable_items.keys()) - tuned
            for name in leftovers:
                template = original_self.tunable_items[name]
                tuple_value = template.default
                value[name] = tuple_value
        constructed_value = original_self._create_dict(value, original_self.locked_args)
        return constructed_value

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def _variant_load_etree_node(original_self, node, source, expect_error):
        if node is None:
            return original_self.default
        value = None
        mtg = get_manager()
        variant = node.get(LoadingAttributes.VariantType, original_self._variant_default)
        if variant is not None:
            if variant in original_self.locked_args:
                value = original_self.locked_args[variant]
            else:
                value = None
                template = original_self.tunable_items.get(variant)
                if template is None:
                    TuningWatcher.get().process_log_message('Variant is set to a type that does not exist: {} in {}.', variant, source)
                    return original_self._variant_default
                node_children = list(node)
                if node_children:
                    child_node = node_children[0]
                    name = child_node.get(LoadingAttributes.Name)
                    if child_node.tag == MergedTuningAttr.Reference:
                        ref_index = child_node.get(MergedTuningAttr.Index)
                        value = mtg.get_tunable(ref_index, template, source)
                        child_node = None
                    else:
                        current_tunable_tag = template.LOADING_TAG_NAME
                        if current_tunable_tag == Tags.TdescFragTag:
                            current_tunable_tag = template.FRAG_TAG_NAME
                        if current_tunable_tag != child_node.tag:
                            tunable_name = node.get(LoadingAttributes.Name, '<Unnamed>')
                            TuningWatcher.get().process_log_message("Incorrectly matched tuning types found in tuning for {} in {}. Expected '{}', got '{}'", tunable_name, source, current_tunable_tag, child_node.tag)
                            TuningWatcher.get().process_log_message('ATTRS 3: {}', child_node.items())
                            _CNTEIXMLValidator._log_etree_node(child_node)
                else:
                    child_node = None
                if value is None:
                    value = template.load_etree_node(child_node, source, expect_error)
                if value is not None:
                    if template._has_callback:
                        if original_self._variant_map is None:
                            original_self._variant_map = {}
                        original_self._variant_map[id(value)] = variant
        return value

    @staticmethod
    @CommonExceptionHandler.catch_exceptions(ModInfo.get_identity())
    def _collection_load_etree_node(original_self, node, source, expect_error):
        (collection_type, collection_fn, final_type, is_final_node) = original_self._get_collection_types()
        if is_final_node(node):
            return original_self.default
        mtg = get_manager()
        tunable_instance = original_self._template
        tunable_name = node.get(LoadingAttributes.Name, '<Unnamed>')
        tunable_collection = collection_type()
        element_index = 0
        for child_node in node:
            element_index += 1
            value = None
            try:
                if child_node.tag == MergedTuningAttr.Reference:
                    ref_index = child_node.get(MergedTuningAttr.Index)
                    value = mtg.get_tunable(ref_index, tunable_instance, source)
                else:
                    current_tunable_tag = tunable_instance.LOADING_TAG_NAME
                    if current_tunable_tag == Tags.TdescFragTag:
                        current_tunable_tag = tunable_instance.FRAG_TAG_NAME
                    if current_tunable_tag != child_node.tag:
                        TuningWatcher.get().process_log_message("Incorrectly matched tuning types found in tuning for {} in {}. Expected '{}', got '{}'", tunable_name, source, current_tunable_tag, child_node.tag)
                        TuningWatcher.get().process_log_message('ATTRS: {}', child_node.items())
                        _CNTEIXMLValidator._log_etree_node(child_node)
                    value = tunable_instance.load_etree_node(child_node, source, expect_error)
                if False and not original_self.allow_none and value is None:
                    TuningWatcher.get().process_log_message('None entry found in tunable list in {}.\nName: {}\nIndex: {}\nContent:{}', source, tunable_name, element_index, child_node)
                    TuningWatcher.get().process_log_message('Invalid value: {}', child_node.text)
                    _CNTEIXMLValidator._log_etree_node(node)
                else:
                    collection_fn(tunable_collection, value)
            except UnavailablePackSafeResourceError:
                continue
            except TunableMinimumLengthError:
                continue
            except:
                TuningWatcher.get().process_log_message('Error while parsing tuning in {}:', source)
                TuningWatcher.get().process_log_message('Failed to load element for {} (index {}): {}. Skipping.', tunable_name, element_index, child_node)
        if original_self.minlength is not None and len(tunable_collection) < original_self.minlength:
            TuningWatcher.get().process_log_message('Collection {} in {} has fewer than the minimum number of entries.', source, tunable_name)
            raise TunableMinimumLengthError
        return final_type(tunable_collection)


@CommonInjectionUtils.inject_into(ETreeTuningLoader, ETreeTuningLoader._load_tunable.__name__)
def _cntei_load_tunable(original, self, *args, **kwargs):
    from cntei.settings import REBUILD_INVALID_XML
    from cntei.settings import FILTER_TEXT_LIST

    should_override = False
    for text_list in FILTER_TEXT_LIST:
        if text_list in TuningWatcher.get()._name:
            should_override = True
            break
    if REBUILD_INVALID_XML and should_override:
        return _CNTEIXMLValidator._serialization_load_tunable(self, *args, **kwargs)
    return original(self, *args, **kwargs)


@CommonInjectionUtils.inject_into(TunableTuple, TunableTuple.load_etree_node.__name__)
def _cntei_load_etree_node_tuple(original, self, *args, **kwargs):
    from cntei.settings import REBUILD_INVALID_XML
    from cntei.settings import FILTER_TEXT_LIST

    should_override = False
    for text_list in FILTER_TEXT_LIST:
        if text_list in TuningWatcher.get()._name:
            should_override = True
            break
    if REBUILD_INVALID_XML and should_override:
        return _CNTEIXMLValidator._tuple_load_etree_node(self, *args, **kwargs)
    return original(self, *args, **kwargs)


@CommonInjectionUtils.inject_into(TunableVariant, TunableVariant.load_etree_node.__name__)
def _cntei_load_etree_node_variant(original, self, *args, **kwargs):
    from cntei.settings import REBUILD_INVALID_XML
    from cntei.settings import FILTER_TEXT_LIST

    should_override = False
    for text_list in FILTER_TEXT_LIST:
        if text_list in TuningWatcher.get()._name:
            should_override = True
            break
    if REBUILD_INVALID_XML and should_override:
        return _CNTEIXMLValidator._variant_load_etree_node(self, *args, **kwargs)
    return original(self, *args, **kwargs)


@CommonInjectionUtils.inject_into(_TunableCollection, _TunableCollection.load_etree_node.__name__)
def _cntei_load_etree_node_variant(original, self, *args, **kwargs):
    from cntei.settings import REBUILD_INVALID_XML
    from cntei.settings import FILTER_TEXT_LIST

    should_override = False
    for text_list in FILTER_TEXT_LIST:
        if text_list in TuningWatcher.get()._name:
            should_override = True
            break
    if REBUILD_INVALID_XML and should_override:
        return _CNTEIXMLValidator._collection_load_etree_node(self, *args, **kwargs)
    return original(self, *args, **kwargs)
