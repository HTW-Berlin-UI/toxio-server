# coding: utf-8
from sqlalchemy import BigInteger, Column, Date, DateTime, Float, ForeignKey,\
    Index, Integer, LargeBinary, Numeric, SmallInteger, String, Table, Text,\
    Time, VARBINARY, text as raw_text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy


Base = declarative_base()
metadata = Base.metadata


class AclClass(Base):
    __tablename__ = 'acl_classes'

    id = Column(Integer, primary_key=True)
    class_type = Column(String(200, 'utf8_unicode_ci'), nullable=False, unique=True)


class AclEntry(Base):
    __tablename__ = 'acl_entries'
    __table_args__ = (
        Index('IDX_46C8B806EA000B103D9AB4A6DF9183C9', 'class_id', 'object_identity_id', 'security_identity_id'),
        Index('UNIQ_46C8B806EA000B103D9AB4A64DEF17BCE4289BF4', 'class_id', 'object_identity_id', 'field_name', 'ace_order', unique=True)
    )

    id = Column(Integer, primary_key=True)
    class_id = Column(ForeignKey('acl_classes.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    object_identity_id = Column(ForeignKey('acl_object_identities.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    security_identity_id = Column(ForeignKey('acl_security_identities.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    field_name = Column(String(255, 'utf8_unicode_ci'))
    ace_order = Column(SmallInteger, nullable=False)
    mask = Column(Integer, nullable=False)
    granting = Column(Integer, nullable=False)
    granting_strategy = Column(String(30, 'utf8_unicode_ci'), nullable=False)
    audit_success = Column(Integer, nullable=False)
    audit_failure = Column(Integer, nullable=False)

    _class = relationship('AclClass')
    object_identity = relationship('AclObjectIdentity')
    security_identity = relationship('AclSecurityIdentity')


class AclObjectIdentity(Base):
    __tablename__ = 'acl_object_identities'
    __table_args__ = (
        Index('UNIQ_9407E5494B12AD6EA000B10', 'object_identifier', 'class_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    parent_object_identity_id = Column(ForeignKey('acl_object_identities.id'), index=True)
    class_id = Column(Integer, nullable=False)
    object_identifier = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    entries_inheriting = Column(Integer, nullable=False)

    parent_object_identity = relationship('AclObjectIdentity', remote_side=[id])
    object_identitys = relationship(
        'AclObjectIdentity',
        secondary='acl_object_identity_ancestors',
        primaryjoin='AclObjectIdentity.id == acl_object_identity_ancestors.c.ancestor_id',
        secondaryjoin='AclObjectIdentity.id == acl_object_identity_ancestors.c.object_identity_id'
    )


t_acl_object_identity_ancestors = Table(
    'acl_object_identity_ancestors', metadata,
    Column('object_identity_id', ForeignKey('acl_object_identities.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('ancestor_id', ForeignKey('acl_object_identities.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
)


class AclSecurityIdentity(Base):
    __tablename__ = 'acl_security_identities'
    __table_args__ = (
        Index('UNIQ_8835EE78772E836AF85E0677', 'identifier', 'username', unique=True),
    )

    id = Column(Integer, primary_key=True)
    identifier = Column(String(200, 'utf8_unicode_ci'), nullable=False)
    username = Column(Integer, nullable=False)


class AkeneoBatchJobExecution(Base):
    __tablename__ = 'akeneo_batch_job_execution'

    id = Column(Integer, primary_key=True)
    job_instance_id = Column(ForeignKey('akeneo_batch_job_instance.id', ondelete='CASCADE'), nullable=False, index=True)
    status = Column(Integer, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    create_time = Column(DateTime)
    updated_time = Column(DateTime)
    exit_code = Column(String(255, 'utf8_unicode_ci'))
    exit_description = Column(String(collation='utf8_unicode_ci'))
    failure_exceptions = Column(String(collation='utf8_unicode_ci'))
    log_file = Column(String(255, 'utf8_unicode_ci'))
    pid = Column(Integer)
    user = Column(String(255, 'utf8_unicode_ci'))

    job_instance = relationship('AkeneoBatchJobInstance')


class AkeneoBatchJobInstance(Base):
    __tablename__ = 'akeneo_batch_job_instance'

    id = Column(Integer, primary_key=True)
    code = Column(String(100, 'utf8_unicode_ci'), nullable=False, unique=True)
    label = Column(String(255, 'utf8_unicode_ci'))
    alias = Column(String(50, 'utf8_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    connector = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    rawConfiguration = Column(String(collation='utf8_unicode_ci'), nullable=False)


class AkeneoBatchMappingField(Base):
    __tablename__ = 'akeneo_batch_mapping_field'

    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('akeneo_batch_mapping_item.id'), index=True)
    source = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    destination = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    identifier = Column(Integer, nullable=False)

    item = relationship('AkeneoBatchMappingItem')


class AkeneoBatchMappingItem(Base):
    __tablename__ = 'akeneo_batch_mapping_item'

    id = Column(Integer, primary_key=True)


class AkeneoBatchStepExecution(Base):
    __tablename__ = 'akeneo_batch_step_execution'

    id = Column(Integer, primary_key=True)
    job_execution_id = Column(ForeignKey('akeneo_batch_job_execution.id', ondelete='CASCADE'), index=True)
    step_name = Column(String(100, 'utf8_unicode_ci'))
    status = Column(Integer, nullable=False)
    read_count = Column(Integer, nullable=False)
    write_count = Column(Integer, nullable=False)
    filter_count = Column(Integer, nullable=False)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    exit_code = Column(String(255, 'utf8_unicode_ci'))
    exit_description = Column(String(collation='utf8_unicode_ci'))
    terminate_only = Column(Integer)
    failure_exceptions = Column(String(collation='utf8_unicode_ci'))
    errors = Column(String(collation='utf8_unicode_ci'), nullable=False)
    summary = Column(String(collation='utf8_unicode_ci'), nullable=False)

    job_execution = relationship('AkeneoBatchJobExecution')


class AkeneoBatchWarning(Base):
    __tablename__ = 'akeneo_batch_warning'

    id = Column(Integer, primary_key=True)
    step_execution_id = Column(ForeignKey('akeneo_batch_step_execution.id', ondelete='CASCADE'), index=True)
    name = Column(String(100, 'utf8_unicode_ci'))
    reason = Column(String(collation='utf8_unicode_ci'))
    reason_parameters = Column(String(collation='utf8_unicode_ci'), nullable=False)
    item = Column(String(collation='utf8_unicode_ci'), nullable=False)

    step_execution = relationship('AkeneoBatchStepExecution')


class ChemScanAccidentRating(Base):
    __tablename__ = 'chem_scan_accident_rating'

    id = Column(Integer, primary_key=True)
    number = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    property = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    qty_threshold_1 = Column(Integer, nullable=False)
    qty_threshold_2 = Column(Integer, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanAgw(Base):
    __tablename__ = 'chem_scan_agw'

    id = Column(Integer, primary_key=True)
    substance_group = Column(String(collation='utf8_unicode_ci'))
    eg = Column(String(255, 'utf8_unicode_ci'))
    cas = Column(String(255, 'utf8_unicode_ci'))
    mlm3 = Column(String(255, 'utf8_unicode_ci'))
    mgm3 = Column(String(255, 'utf8_unicode_ci'))
    kw = Column(String(255, 'utf8_unicode_ci'))
    comments = Column(String(collation='utf8_unicode_ci'))
    month = Column(Date)
    update_date = Column(Date)
    regulation = Column(String(255, 'utf8_unicode_ci'))
    agw = Column(String(255, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanAgwComment(Base):
    __tablename__ = 'chem_scan_agw_comment'

    id = Column(Integer, primary_key=True)
    cipher = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    text = Column(String(collation='utf8_unicode_ci'), nullable=False)


class ChemScanArbmedvv(Base):
    __tablename__ = 'chem_scan_arbmedvv'

    id = Column(Integer, primary_key=True)
    eg = Column(String(255, 'utf8_unicode_ci'))
    cas = Column(String(255, 'utf8_unicode_ci'))
    examination = Column(String(255, 'utf8_unicode_ci'))
    update_date = Column(Date)
    regulation = Column(String(255, 'utf8_unicode_ci'))
    type = Column(String(255, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanAttribute(Base):
    __tablename__ = 'chem_scan_attribute'
    __table_args__ = (
        Index('chem_scan_attribute_lpc_uq', 'level', 'position', 'character', unique=True),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    level = Column(Integer, nullable=False, index=True)
    position = Column(Integer, nullable=False, index=True)
    character = Column(String(1, 'utf8_unicode_ci'), nullable=False, index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    r_rates = relationship('ChemScanRRate', secondary='chem_scan_attribute_r_rate')
    hss = relationship('ChemScanH', secondary='chem_scan_hs_attribute')


t_chem_scan_attribute_r_rate = Table(
    'chem_scan_attribute_r_rate', metadata,
    Column('r_rate_id', ForeignKey('chem_scan_r_rate.id'), nullable=False, index=True),
    Column('attribute_id', ForeignKey('chem_scan_attribute.id'), nullable=False, index=True)
)


class ChemScanAttributeRule(Base):
    __tablename__ = 'chem_scan_attribute_rule'

    id = Column(Integer, primary_key=True)
    attribute_id = Column(ForeignKey('chem_scan_attribute.id'), nullable=False, index=True)
    rule = Column(String(collation='utf8_unicode_ci'), nullable=False)

    attribute = relationship('ChemScanAttribute')


class ChemScanBgw(Base):
    __tablename__ = 'chem_scan_bgw'

    id = Column(Integer, primary_key=True)
    substance_group = Column(String(collation='utf8_unicode_ci'))
    eg = Column(String(255, 'utf8_unicode_ci'))
    cas = Column(String(255, 'utf8_unicode_ci'))
    parameter = Column(String(255, 'utf8_unicode_ci'))
    exam = Column(String(255, 'utf8_unicode_ci'))
    sampling_time = Column(String(255, 'utf8_unicode_ci'))
    vo = Column(String(255, 'utf8_unicode_ci'))
    specificity = Column(String(255, 'utf8_unicode_ci'))
    date = Column(Date)
    bgw = Column(String(255, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanBreatheEmkg(Base):
    __tablename__ = 'chem_scan_breathe_emkg'

    id = Column(Integer, primary_key=True)
    code = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    hg = Column(SmallInteger, nullable=False)
    qg = Column(SmallInteger, nullable=False)
    eg = Column(SmallInteger, nullable=False)
    rating = Column(SmallInteger, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanBreatheEmkgRule(Base):
    __tablename__ = 'chem_scan_breathe_emkg_rule'

    id = Column(Integer, primary_key=True)
    breathe_emkg_rating = Column(SmallInteger, nullable=False)
    rule = Column(String(collation='utf8_unicode_ci'), nullable=False)


class ChemScanCatalog(Base):
    __tablename__ = 'chem_scan_catalog'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    code = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    table_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    entity = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanClp(Base):
    __tablename__ = 'chem_scan_clp'
    __table_args__ = (
        Index('eg_2', 'eg', 'cas'),
    )

    id = Column(Integer, primary_key=True)
    index_nr = Column(String(255, 'utf8_unicode_ci'))
    substance_group = Column(String(collation='utf8_unicode_ci'))
    eg = Column(String(255, 'utf8_unicode_ci'), index=True)
    cas = Column(String(255, 'utf8_unicode_ci'), index=True)
    name = Column(String(collation='utf8_unicode_ci'))
    update_date = Column(Date)
    regulation = Column(String(255, 'utf8_unicode_ci'))
    comments = Column(String(255, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanClpIndex(Base):
    __tablename__ = 'chem_scan_clp_index'

    id = Column(Integer, primary_key=True)
    hazard_note_symbol_id = Column(ForeignKey('chem_scan_symbol.id'), index=True)
    hazard_note_sign_id = Column(ForeignKey('chem_scan_r_rate.id'), index=True)
    hazard_note_rating_id = Column(ForeignKey('chem_scan_r_rate.id'), index=True)
    index_nr = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    hazard_rating_symbol = Column(String(255, 'utf8_unicode_ci'))
    hazard_attribute = Column(String(255, 'utf8_unicode_ci'))
    specification = Column(String(255, 'utf8_unicode_ci'))
    annotation = Column(String(255, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    hazard_note_rating = relationship('ChemScanRRate', primaryjoin='ChemScanClpIndex.hazard_note_rating_id == ChemScanRRate.id')
    hazard_note_sign = relationship('ChemScanRRate', primaryjoin='ChemScanClpIndex.hazard_note_sign_id == ChemScanRRate.id')
    hazard_note_symbol = relationship('ChemScanSymbol')


class ChemScanDocument(Base):
    __tablename__ = 'chem_scan_document'

    id = Column(Integer, primary_key=True)
    document_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    code = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_by = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    document = relationship('OroAttachmentFile')


class ChemScanExGroup(Base):
    __tablename__ = 'chem_scan_ex_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    boiling_point_min = Column(Integer)
    boiling_point_max = Column(Integer)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanFireEmkg(Base):
    __tablename__ = 'chem_scan_fire_emkg'

    id = Column(Integer, primary_key=True)
    code = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    hg = Column(SmallInteger, nullable=False)
    qg = Column(SmallInteger, nullable=False)
    eg = Column(SmallInteger, nullable=False)
    ag = Column(SmallInteger, nullable=False)
    rating = Column(SmallInteger, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanFireEmkgRule(Base):
    __tablename__ = 'chem_scan_fire_emkg_rule'

    id = Column(Integer, primary_key=True)
    fire_emkg_rating = Column(SmallInteger, nullable=False)
    rule = Column(String(collation='utf8_unicode_ci'), nullable=False)


class ChemScanHazardNote(Base):
    __tablename__ = 'chem_scan_hazard_note'

    id = Column(Integer, primary_key=True)
    note = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanHazardRating(Base):
    __tablename__ = 'chem_scan_hazard_rating'

    id = Column(Integer, primary_key=True)
    rating = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    hss = relationship('ChemScanH', secondary='chem_scan_hs_hazard_rating')


class ChemScanHotkey(Base):
    __tablename__ = 'chem_scan_hotkeys'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), index=True)
    ctrl_key = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    alt_key = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    char_code = Column(SmallInteger, nullable=False)
    route = Column(String(255, 'utf8_unicode_ci'), nullable=False)

    user = relationship('OroUser')


class ChemScanH(Base):
    __tablename__ = 'chem_scan_hs'

    id = Column(Integer, primary_key=True)
    manufacturer_id = Column(ForeignKey('chem_scan_man_supplier.id'), nullable=False, index=True)
    lager_class_id = Column(ForeignKey('chem_scan_lager_class.id'), index=True)
    hazard_note_id = Column(ForeignKey('chem_scan_hazard_note.id'), index=True)
    waste_key_id = Column(ForeignKey('chem_scan_waste_key.id'), index=True)
    unclean_packaging_id = Column(ForeignKey('chem_scan_waste_key.id'), index=True)
    clean_packaging_id = Column(ForeignKey('chem_scan_waste_key.id'), index=True)
    un_number_id = Column(ForeignKey('chem_scan_un_number.id'), index=True)
    hazard_key = Column(String(255, 'utf8_unicode_ci'))
    active = Column(SmallInteger, nullable=False, server_default=raw_text("1"))
    hs_number = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    signal_word = Column(String(255, 'utf8_unicode_ci'))
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    form = Column(String(255, 'utf8_unicode_ci'))
    water_hazard_class = Column(Integer)
    accident_rating_id = Column(Integer)
    purpose_sds = Column(String(collation='utf8_unicode_ci'))
    approved = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    draft = Column(SmallInteger, server_default=raw_text("0"))
    locked = Column(SmallInteger, server_default=raw_text("0"))
    emergency_phone = Column(String(255, 'utf8_unicode_ci'))
    other_hazard = Column(String(collation='utf8_unicode_ci'))
    first_aid_note_general = Column(String(collation='utf8_unicode_ci'))
    first_aid_note_breathe = Column(String(collation='utf8_unicode_ci'))
    first_aid_note_skin = Column(String(collation='utf8_unicode_ci'))
    first_aid_note_eye = Column(String(collation='utf8_unicode_ci'))
    first_aid_note_swallow = Column(String(collation='utf8_unicode_ci'))
    first_aid_additional_note = Column(String(collation='utf8_unicode_ci'))
    symptoms = Column(String(collation='utf8_unicode_ci'))
    doctor_help = Column(String(collation='utf8_unicode_ci'))
    suitable_exauhsting = Column(String(collation='utf8_unicode_ci'))
    not_suitable_exauhsting = Column(String(collation='utf8_unicode_ci'))
    special_fire_hazard = Column(String(collation='utf8_unicode_ci'))
    firefighting_note = Column(String(collation='utf8_unicode_ci'))
    firefighting_additional_note = Column(String(collation='utf8_unicode_ci'))
    personal_safeguard_release = Column(String(collation='utf8_unicode_ci'))
    env_safeguard_release = Column(String(collation='utf8_unicode_ci'))
    clean_retain_material = Column(String(collation='utf8_unicode_ci'))
    excrete_additional_note = Column(String(collation='utf8_unicode_ci'))
    note_safe_dealing = Column(String(collation='utf8_unicode_ci'))
    note_fire_ex_guard = Column(String(collation='utf8_unicode_ci'))
    note_storage = Column(String(collation='utf8_unicode_ci'))
    note_storage_additional = Column(String(collation='utf8_unicode_ci'))
    specific_usage = Column(String(collation='utf8_unicode_ci'))
    technical_pa = Column(String(collation='utf8_unicode_ci'))
    breathe_guard = Column(String(collation='utf8_unicode_ci'))
    breathe_proposed_equipment = Column(Text(collation='utf8_unicode_ci'))
    body_guard = Column(String(collation='utf8_unicode_ci'))
    body_proposed_equipment = Column(Text(collation='utf8_unicode_ci'))
    hand_guard = Column(String(collation='utf8_unicode_ci'))
    hand_proposed_equipment = Column(Text(collation='utf8_unicode_ci'))
    eye_guard = Column(String(collation='utf8_unicode_ci'))
    eye_proposed_equipment = Column(Text(collation='utf8_unicode_ci'))
    density = Column(Numeric(10, 4))
    target_organ_toxicity_multi = Column(String(collation='utf8_unicode_ci'))
    relative_density = Column(Numeric(10, 4))
    dusting = Column(String(255, 'utf8_unicode_ci'))
    boiling_point = Column(Numeric(10, 2))
    flame_point = Column(Numeric(10, 2))
    ue_percent = Column(Numeric(10, 2))
    oe_percent = Column(Numeric(10, 2))
    flammable = Column(SmallInteger)
    appearance = Column(String(collation='utf8_unicode_ci'))
    look = Column(String(collation='utf8_unicode_ci'))
    smell = Column(String(collation='utf8_unicode_ci'))
    steam_pressure = Column(Numeric(10, 4))
    inflammability = Column(String(collation='utf8_unicode_ci'))
    odor_threshold = Column(String(collation='utf8_unicode_ci'))
    solubility = Column(String(collation='utf8_unicode_ci'))
    oxidizing_features = Column(String(collation='utf8_unicode_ci'))
    ph_value = Column(Numeric(10, 2))
    steam_density = Column(Numeric(12, 4))
    melting_fridge_point = Column(Numeric(10, 2))
    self_decomposition_temp = Column(Numeric(10, 2))
    evaporation_speed = Column(Numeric(10, 2))
    distribution_octan_water = Column(Numeric(10, 2))
    viscosity = Column(Numeric(10, 4))
    viscosity_dynamic = Column(Numeric(10, 4))
    decomposition_temp = Column(Numeric(10, 2))
    explosive_features = Column(String(collation='utf8_unicode_ci'))
    other_features = Column(String(collation='utf8_unicode_ci'))
    reactivity = Column(String(collation='utf8_unicode_ci'))
    chemical_stability = Column(String(collation='utf8_unicode_ci'))
    possible_hazard_reactions = Column(String(collation='utf8_unicode_ci'))
    conditions_to_avoid = Column(String(collation='utf8_unicode_ci'))
    incompatible_materials = Column(String(collation='utf8_unicode_ci'))
    hazardous_decomp_prod = Column(String(collation='utf8_unicode_ci'))
    note_toxicity = Column(String(collation='utf8_unicode_ci'))
    stimulation_effect = Column(String(collation='utf8_unicode_ci'))
    caustic_effect = Column(String(collation='utf8_unicode_ci'))
    sensitization = Column(String(collation='utf8_unicode_ci'))
    carcinogenicity = Column(String(collation='utf8_unicode_ci'))
    mutagenicity = Column(String(collation='utf8_unicode_ci'))
    reproduction_toxicity = Column(String(collation='utf8_unicode_ci'))
    note_toxicity_additional = Column(String(collation='utf8_unicode_ci'))
    env_toxicity = Column(String(collation='utf8_unicode_ci'))
    persistence = Column(String(collation='utf8_unicode_ci'))
    bioaccumulation = Column(String(collation='utf8_unicode_ci'))
    mobility_in_soil = Column(String(collation='utf8_unicode_ci'))
    pbt_vpvb = Column(String(collation='utf8_unicode_ci'))
    other_harmful_impact = Column(String(collation='utf8_unicode_ci'))
    waste_procedure = Column(String(collation='utf8_unicode_ci'))
    un_shipping_label = Column(String(collation='utf8_unicode_ci'))
    packing_group_id = Column(Integer)
    adr_rid = Column(SmallInteger)
    icao_ti = Column(SmallInteger)
    special_caution_for_user = Column(String(collation='utf8_unicode_ci'))
    marpol = Column(String(collation='utf8_unicode_ci'))
    voc_amount = Column(Integer)
    safety_assesment = Column(String(collation='utf8_unicode_ci'))
    other_notes = Column(String(collation='utf8_unicode_ci'))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    aspiration_hazard = Column(String(collation='utf8_unicode_ci'))
    target_organ_toxicity_single = Column(String(collation='utf8_unicode_ci'))
    env_exposition = Column(String(collation='utf8_unicode_ci'))
    proposed_equipment = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    clean_packaging = relationship('ChemScanWasteKey', primaryjoin='ChemScanH.clean_packaging_id == ChemScanWasteKey.id')
    hazard_note = relationship('ChemScanHazardNote')
    lager_class = relationship('ChemScanLagerClas')
    manufacturer = relationship('ChemScanManSupplier')
    un_number = relationship('ChemScanUnNumber')
    unclean_packaging = relationship('ChemScanWasteKey', primaryjoin='ChemScanH.unclean_packaging_id == ChemScanWasteKey.id')
    waste_key = relationship('ChemScanWasteKey', primaryjoin='ChemScanH.waste_key_id == ChemScanWasteKey.id')
    r_rates = relationship('ChemScanRRate', secondary='chem_scan_hs_r_rate')
    symbols = relationship('ChemScanSymbol', secondary='chem_scan_hs_symbol')
    sp_rates = relationship('ChemScanSpRate', secondary='chem_scan_hs_sp_rate')


t_chem_scan_hs_attribute = Table(
    'chem_scan_hs_attribute', metadata,
    Column('hs_id', ForeignKey('chem_scan_hs.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('attribute_id', ForeignKey('chem_scan_attribute.id', ondelete='CASCADE'), nullable=False, index=True)
)


class ChemScanHsCalculation(Base):
    __tablename__ = 'chem_scan_hs_calculation'

    id = Column(Integer, primary_key=True)
    hs_id = Column(ForeignKey('chem_scan_hs.id', ondelete='CASCADE'), nullable=False, index=True)
    lager_class_id = Column(ForeignKey('chem_scan_lager_class.id'), index=True)
    ex_group_id = Column(ForeignKey('chem_scan_ex_group.id'), index=True)
    water_hazard_class = Column(Integer)

    ex_group = relationship('ChemScanExGroup')
    hs = relationship('ChemScanH')
    lager_class = relationship('ChemScanLagerClas')


class ChemScanHsCheck(Base):
    __tablename__ = 'chem_scan_hs_check'

    id = Column(Integer, primary_key=True)
    hs_id = Column(ForeignKey('chem_scan_hs.id', ondelete='CASCADE'), nullable=False, index=True)
    w_factor = Column(Integer, nullable=False, server_default=raw_text("0"))
    fire_hazard = Column(Integer, nullable=False, server_default=raw_text("0"))
    env_hazard = Column(Integer, nullable=False, server_default=raw_text("0"))
    exc_hazard = Column(Integer, nullable=False, server_default=raw_text("0"))

    hs = relationship('ChemScanH')


class ChemScanHsCheckRuleEnv(Base):
    __tablename__ = 'chem_scan_hs_check_rule_env'

    id = Column(Integer, primary_key=True)
    incl_r_rate_id = Column(ForeignKey('chem_scan_r_rate.id'), index=True)
    excl_r_rate_id = Column(ForeignKey('chem_scan_r_rate.id'), index=True)
    incl_symbol_id = Column(ForeignKey('chem_scan_symbol.id'), index=True)
    excl_symbol_id = Column(ForeignKey('chem_scan_symbol.id'), index=True)
    rating = Column(Integer, nullable=False)
    whc = Column(SmallInteger)
    form = Column(String(100, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    excl_r_rate = relationship('ChemScanRRate', primaryjoin='ChemScanHsCheckRuleEnv.excl_r_rate_id == ChemScanRRate.id')
    excl_symbol = relationship('ChemScanSymbol', primaryjoin='ChemScanHsCheckRuleEnv.excl_symbol_id == ChemScanSymbol.id')
    incl_r_rate = relationship('ChemScanRRate', primaryjoin='ChemScanHsCheckRuleEnv.incl_r_rate_id == ChemScanRRate.id')
    incl_symbol = relationship('ChemScanSymbol', primaryjoin='ChemScanHsCheckRuleEnv.incl_symbol_id == ChemScanSymbol.id')


class ChemScanHsCheckRuleExc(Base):
    __tablename__ = 'chem_scan_hs_check_rule_exc'

    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    form = Column(String(100, 'utf8_unicode_ci'))
    steam_pressure_min = Column(Integer)
    steam_pressure_max = Column(Integer)
    dusting = Column(SmallInteger)


class ChemScanHsCheckRuleFire(Base):
    __tablename__ = 'chem_scan_hs_check_rule_fire'

    id = Column(Integer, primary_key=True)
    incl_r_rate_id = Column(ForeignKey('chem_scan_r_rate.id'), index=True)
    excl_r_rate_id = Column(ForeignKey('chem_scan_r_rate.id'), index=True)
    rating = Column(Integer, nullable=False)
    form = Column(String(100, 'utf8_unicode_ci'))
    flame_point_min = Column(Integer)
    flame_point_max = Column(Integer)

    excl_r_rate = relationship('ChemScanRRate', primaryjoin='ChemScanHsCheckRuleFire.excl_r_rate_id == ChemScanRRate.id')
    incl_r_rate = relationship('ChemScanRRate', primaryjoin='ChemScanHsCheckRuleFire.incl_r_rate_id == ChemScanRRate.id')


class ChemScanHsHa(Base):
    __tablename__ = 'chem_scan_hs_ha'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    created_by = Column(Integer)
    approved_at = Column(Date)
    number = Column(String(255, 'utf8_unicode_ci'))
    name = Column(String(255, 'utf8_unicode_ci'))
    responsible_person_id = Column(ForeignKey('chem_scan_person.id'), index=True)
    status = Column(String(255, 'utf8_unicode_ci'))
    revision = Column(String(255, 'utf8_unicode_ci'))
    comment = Column(Text(collation='utf8_unicode_ci'))
    check_period = Column(String(255, 'utf8_unicode_ci'))
    next_check = Column(Date)
    work_med_prev_needed = Column(SmallInteger, server_default=raw_text("0"))
    work_med_prev_comment = Column(String(collation='utf8_unicode_ci'))
    oper_inst_needed = Column(SmallInteger, server_default=raw_text("0"))
    oper_inst_comment = Column(String(collation='utf8_unicode_ci'))
    instr_needed = Column(SmallInteger, server_default=raw_text("0"))
    instr_comment = Column(String(collation='utf8_unicode_ci'))
    eye_equip = Column(String(collation='utf8_unicode_ci'))
    eye_comment = Column(String(collation='utf8_unicode_ci'))
    breathe_equip = Column(String(collation='utf8_unicode_ci'))
    breathe_comment = Column(String(collation='utf8_unicode_ci'))
    hand_equip = Column(String(collation='utf8_unicode_ci'))
    hand_comment = Column(String(collation='utf8_unicode_ci'))
    body_equip = Column(String(collation='utf8_unicode_ci'))
    body_comment = Column(String(collation='utf8_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    file_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    file = relationship('OroAttachmentFile')
    organization = relationship('OroOrganization')
    responsible_person = relationship('ChemScanPerson')
    hs_usages = relationship('ChemScanHsUsage', secondary='chem_scan_hs_ha_usages')
    persons = relationship('ChemScanPerson', secondary='chem_scan_hs_ha_support_person')
    pa_sources = relationship('ChemScanPaSource', secondary='chem_scan_hs_ha_source')


class ChemScanHsHaDoc(Base):
    __tablename__ = 'chem_scan_hs_ha_docs'

    id = Column(Integer, primary_key=True)
    file_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    hs_ha_id = Column(ForeignKey('chem_scan_hs_ha.id', ondelete='CASCADE'), nullable=False, index=True)
    type = Column(String(255, 'utf8_unicode_ci'))
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    file = relationship('OroAttachmentFile')
    hs_ha = relationship('ChemScanHsHa')


class ChemScanHsHaOi(Base):
    __tablename__ = 'chem_scan_hs_ha_oi'

    id = Column(Integer, primary_key=True)
    hs_ha_id = Column(ForeignKey('chem_scan_hs_ha.id', ondelete='CASCADE'), nullable=False, index=True)
    hs_ha_pa_id = Column(ForeignKey('chem_scan_hs_ha_pa.id', ondelete='CASCADE'), index=True)
    responsible_person_id = Column(ForeignKey('chem_scan_position_person.id', ondelete='SET NULL'), index=True)
    operation_instruction = Column(String(collation='utf8_unicode_ci'), nullable=False)
    status = Column(String(255, 'utf8_unicode_ci'), nullable=False)

    hs_ha = relationship('ChemScanHsHa')
    hs_ha_pa = relationship('ChemScanHsHaPa')
    responsible_person = relationship('ChemScanPositionPerson')


class ChemScanHsHaPa(Base):
    __tablename__ = 'chem_scan_hs_ha_pa'

    id = Column(Integer, primary_key=True)
    hs_ha_id = Column(ForeignKey('chem_scan_hs_ha.id', ondelete='CASCADE'), nullable=False, index=True)
    number = Column(String(255, 'utf8_unicode_ci'))
    protection_action = Column(String(collation='utf8_unicode_ci'), nullable=False)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    is_operation_instruction = Column(SmallInteger, server_default=raw_text("0"))
    is_activity = Column(SmallInteger, server_default=raw_text("0"))
    comment = Column(String(collation='utf8_unicode_ci'))
    responsible_person_id = Column(Integer)
    status = Column(String(255, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    hs_ha = relationship('ChemScanHsHa')
    pas = relationship('ChemScanPa', secondary='chem_scan_hs_ha_pa_source')


class ChemScanHsHaPaActivity(Base):
    __tablename__ = 'chem_scan_hs_ha_pa_activity'

    id = Column(Integer, primary_key=True)
    hs_ha_id = Column(ForeignKey('chem_scan_hs_ha.id', ondelete='CASCADE'), index=True)
    hs_ha_pa_id = Column(ForeignKey('chem_scan_hs_ha_pa.id', ondelete='CASCADE'), nullable=False, index=True)
    number = Column(String(255, 'utf8_unicode_ci'))
    parent_activity_id = Column(ForeignKey('chem_scan_hs_ha_pa_activity.id', ondelete='CASCADE'), index=True)
    position_person_id = Column(ForeignKey('chem_scan_position_person.id', ondelete='CASCADE'), index=True)
    organization_unit_id = Column(ForeignKey('chem_scan_organization_unit.id', ondelete='CASCADE'), index=True)
    activity = Column(String(collation='utf8_unicode_ci'))
    comment = Column(String(collation='utf8_unicode_ci'))
    efficiency_check = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    target_date = Column(Date)
    status = Column(String(255, 'utf8_unicode_ci'))

    hs_ha = relationship('ChemScanHsHa')
    hs_ha_pa = relationship('ChemScanHsHaPa')
    organization_unit = relationship('ChemScanOrganizationUnit')
    parent_activity = relationship('ChemScanHsHaPaActivity', remote_side=[id])
    position_person = relationship('ChemScanPositionPerson')


t_chem_scan_hs_ha_pa_source = Table(
    'chem_scan_hs_ha_pa_source', metadata,
    Column('hs_ha_pa_id', ForeignKey('chem_scan_hs_ha_pa.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('pa_id', ForeignKey('chem_scan_pa.id', ondelete='CASCADE'), nullable=False, index=True)
)


t_chem_scan_hs_ha_plants = Table(
    'chem_scan_hs_ha_plants', metadata,
    Column('hs_ha_id', ForeignKey('chem_scan_hs_ha.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('hs_plant_id', Integer, nullable=False, index=True)
)


t_chem_scan_hs_ha_source = Table(
    'chem_scan_hs_ha_source', metadata,
    Column('hs_ha_id', ForeignKey('chem_scan_hs_ha.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('pa_source_id', ForeignKey('chem_scan_pa_source.id', ondelete='CASCADE'), nullable=False, index=True)
)


t_chem_scan_hs_ha_support_person = Table(
    'chem_scan_hs_ha_support_person', metadata,
    Column('hs_ha_id', ForeignKey('chem_scan_hs_ha.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('person_id', ForeignKey('chem_scan_person.id', ondelete='CASCADE'), nullable=False, index=True)
)


t_chem_scan_hs_ha_usages = Table(
    'chem_scan_hs_ha_usages', metadata,
    Column('hs_ha_id', ForeignKey('chem_scan_hs_ha.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('hs_usage_id', ForeignKey('chem_scan_hs_usage.id', ondelete='CASCADE'), nullable=False, index=True)
)


t_chem_scan_hs_hazard_rating = Table(
    'chem_scan_hs_hazard_rating', metadata,
    Column('hs_id', ForeignKey('chem_scan_hs.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('hazard_rating_id', ForeignKey('chem_scan_hazard_rating.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
)


class ChemScanHsOi(Base):
    __tablename__ = 'chem_scan_hs_oi'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    created_by = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    approved_at = Column(Date)
    hs_ha_id = Column(ForeignKey('chem_scan_hs_ha.id', ondelete='CASCADE'), nullable=False, index=True)
    responsible_person_id = Column(ForeignKey('chem_scan_person.id', ondelete='SET NULL'), index=True)
    number = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    revision = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    emergency_number = Column(String(255, 'utf8_unicode_ci'))
    status = Column(String(255, 'utf8_unicode_ci'))
    check_period = Column(String(255, 'utf8_unicode_ci'))
    comment = Column(Text(collation='utf8_unicode_ci'))
    reactivity = Column(String(collation='utf8_unicode_ci'))
    chemical_stability = Column(String(collation='utf8_unicode_ci'))
    possible_hazard_reactions = Column(String(collation='utf8_unicode_ci'))
    conditions_to_avoid = Column(String(collation='utf8_unicode_ci'))
    incompatible_materials = Column(String(collation='utf8_unicode_ci'))
    hazardous_decomp_prod = Column(String(collation='utf8_unicode_ci'))
    reactivity_summary = Column(String(collation='utf8_unicode_ci'))
    note_safe_dealing = Column(String(collation='utf8_unicode_ci'))
    note_fire_ex_guard = Column(String(collation='utf8_unicode_ci'))
    note_storage = Column(String(collation='utf8_unicode_ci'))
    specific_usage = Column(String(collation='utf8_unicode_ci'))
    note_storage_additional = Column(String(collation='utf8_unicode_ci'))
    storage_summary = Column(String(collation='utf8_unicode_ci'))
    breathe_protection = Column(String(collation='utf8_unicode_ci'))
    hand_protection = Column(String(collation='utf8_unicode_ci'))
    eye_protection = Column(String(collation='utf8_unicode_ci'))
    body_protection = Column(String(collation='utf8_unicode_ci'))
    personal_safeguard_release = Column(String(collation='utf8_unicode_ci'))
    env_safe_guard_release = Column(String(collation='utf8_unicode_ci'))
    clean_retain_material = Column(String(collation='utf8_unicode_ci'))
    excrete_additional_note = Column(String(collation='utf8_unicode_ci'))
    excrete_summary = Column(String(collation='utf8_unicode_ci'))
    disposal_summary = Column(String(collation='utf8_unicode_ci'))
    suitable_exauhsting = Column(String(collation='utf8_unicode_ci'))
    not_suitable_exauhsting = Column(String(collation='utf8_unicode_ci'))
    special_fire_hazard = Column(String(collation='utf8_unicode_ci'))
    firefighting_note = Column(String(collation='utf8_unicode_ci'))
    firefighting_additional_note = Column(String(collation='utf8_unicode_ci'))
    fire_summary = Column(String(collation='utf8_unicode_ci'))
    hygiene_summary = Column(String(collation='utf8_unicode_ci'))
    first_aid_note_general = Column(String(collation='utf8_unicode_ci'))
    first_aid_note_breathe = Column(String(collation='utf8_unicode_ci'))
    first_aid_note_skin = Column(String(collation='utf8_unicode_ci'))
    first_aid_note_eye = Column(String(collation='utf8_unicode_ci'))
    first_aid_note_swallow = Column(String(collation='utf8_unicode_ci'))
    first_aid_additional_note = Column(String(collation='utf8_unicode_ci'))
    symptoms = Column(String(collation='utf8_unicode_ci'))
    doctor_help = Column(String(collation='utf8_unicode_ci'))
    first_aid_general_pa = Column(String(collation='utf8_unicode_ci'))
    first_aid_breathe_pa = Column(String(collation='utf8_unicode_ci'))
    first_aid_skin_pa = Column(String(collation='utf8_unicode_ci'))
    first_aid_eye_pa = Column(String(collation='utf8_unicode_ci'))
    first_aid_swallow_pa = Column(String(collation='utf8_unicode_ci'))
    first_aid_additional_info = Column(String(collation='utf8_unicode_ci'))
    additional_information = Column(String(collation='utf8_unicode_ci'))
    print_settings = Column(String(collation='utf8_unicode_ci'))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    file_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    oro_user = relationship('OroUser')
    file = relationship('OroAttachmentFile')
    hs_ha = relationship('ChemScanHsHa')
    organization = relationship('OroOrganization')
    responsible_person = relationship('ChemScanPerson')
    pictograms = relationship('ChemScanPictogramEscape', secondary='chem_scan_hs_oi_pict_escape')
    pictograms1 = relationship('ChemScanPictogramProh', secondary='chem_scan_hs_oi_pict_proh')
    pictograms2 = relationship('ChemScanPictogramFire', secondary='chem_scan_hs_oi_pict_fire')
    scopes = relationship('ChemScanScope', secondary='chem_scan_hs_oi_scope')
    plants = relationship('ChemScanPlant', secondary='chem_scan_hs_oi_plants')
    pictograms3 = relationship('ChemScanPictogramWarn', secondary='chem_scan_hs_oi_pict_warn')
    hs_usages = relationship('ChemScanHsUsage', secondary='chem_scan_hs_oi_hs_usages')
    pictograms4 = relationship('ChemScanPictogramOffer', secondary='chem_scan_hs_oi_pict_offer')
    organization_units = relationship('ChemScanOrganizationUnit', secondary='chem_scan_hs_oi_ou')


class ChemScanHsOiDoc(Base):
    __tablename__ = 'chem_scan_hs_oi_docs'

    id = Column(Integer, primary_key=True)
    file_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    hs_oi_id = Column(ForeignKey('chem_scan_hs_oi.id', ondelete='CASCADE'), nullable=False, index=True)
    type = Column(String(255, 'utf8_unicode_ci'))
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    file = relationship('OroAttachmentFile')
    hs_oi = relationship('ChemScanHsOi')


t_chem_scan_hs_oi_hs_usages = Table(
    'chem_scan_hs_oi_hs_usages', metadata,
    Column('hs_oi_id', ForeignKey('chem_scan_hs_oi.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('hs_usage_id', ForeignKey('chem_scan_hs_usage.id', ondelete='CASCADE'), nullable=False, index=True)
)


class ChemScanHsOiOi(Base):
    __tablename__ = 'chem_scan_hs_oi_oi'

    id = Column(Integer, primary_key=True)
    hs_oi_id = Column(ForeignKey('chem_scan_hs_oi.id', ondelete='CASCADE'), nullable=False, index=True)
    hs_ha_oi_id = Column(ForeignKey('chem_scan_hs_ha_oi.id', ondelete='CASCADE'), nullable=False, index=True)
    section = Column(String(collation='utf8_unicode_ci'), nullable=False)
    operation_instruction = Column(String(collation='utf8_unicode_ci'), nullable=False)

    hs_ha_oi = relationship('ChemScanHsHaOi')
    hs_oi = relationship('ChemScanHsOi')


t_chem_scan_hs_oi_ou = Table(
    'chem_scan_hs_oi_ou', metadata,
    Column('hs_oi_id', ForeignKey('chem_scan_hs_oi.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('organization_unit_id', ForeignKey('chem_scan_organization_unit.id', ondelete='CASCADE'), nullable=False, index=True)
)


t_chem_scan_hs_oi_pict_escape = Table(
    'chem_scan_hs_oi_pict_escape', metadata,
    Column('hs_oi_id', ForeignKey('chem_scan_hs_oi.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('pictogram_id', ForeignKey('chem_scan_pictogram_escape.id', ondelete='CASCADE'), nullable=False, index=True)
)


t_chem_scan_hs_oi_pict_fire = Table(
    'chem_scan_hs_oi_pict_fire', metadata,
    Column('hs_oi_id', ForeignKey('chem_scan_hs_oi.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('pictogram_id', ForeignKey('chem_scan_pictogram_fire.id', ondelete='CASCADE'), nullable=False, index=True)
)


t_chem_scan_hs_oi_pict_offer = Table(
    'chem_scan_hs_oi_pict_offer', metadata,
    Column('hs_oi_id', ForeignKey('chem_scan_hs_oi.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('pictogram_id', ForeignKey('chem_scan_pictogram_offer.id', ondelete='CASCADE'), nullable=False, index=True)
)


t_chem_scan_hs_oi_pict_proh = Table(
    'chem_scan_hs_oi_pict_proh', metadata,
    Column('hs_oi_id', ForeignKey('chem_scan_hs_oi.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('pictogram_id', ForeignKey('chem_scan_pictogram_proh.id', ondelete='CASCADE'), nullable=False, index=True)
)


t_chem_scan_hs_oi_pict_warn = Table(
    'chem_scan_hs_oi_pict_warn', metadata,
    Column('hs_oi_id', ForeignKey('chem_scan_hs_oi.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('pictogram_id', ForeignKey('chem_scan_pictogram_warn.id', ondelete='CASCADE'), nullable=False, index=True)
)


t_chem_scan_hs_oi_plants = Table(
    'chem_scan_hs_oi_plants', metadata,
    Column('hs_oi_id', ForeignKey('chem_scan_hs_oi.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('plant_id', ForeignKey('chem_scan_plant.id', ondelete='CASCADE'), nullable=False, index=True)
)


t_chem_scan_hs_oi_scope = Table(
    'chem_scan_hs_oi_scope', metadata,
    Column('hs_oi_id', ForeignKey('chem_scan_hs_oi.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('scope_id', ForeignKey('chem_scan_scope.id', ondelete='CASCADE'), nullable=False, index=True)
)


class ChemScanHsOrganization(Base):
    __tablename__ = 'chem_scan_hs_organization'

    id = Column(Integer, primary_key=True)
    hs_id = Column(ForeignKey('chem_scan_hs.id', ondelete='CASCADE'), nullable=False, index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    active = Column(SmallInteger, nullable=False)
    substance_group_id = Column(ForeignKey('chem_scan_substance_group.id'), index=True)
    substance_type = Column(String(255, 'utf8_unicode_ci'))
    used_since = Column(Date)
    used_till = Column(Date)
    additional_info_1 = Column(String(collation='utf8_unicode_ci'))
    additional_info_2 = Column(String(collation='utf8_unicode_ci'))
    additional_info_3 = Column(String(collation='utf8_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    hs = relationship('ChemScanH')
    organization = relationship('OroOrganization')
    substance_group = relationship('ChemScanSubstanceGroup')
    position_persons = relationship('ChemScanPositionPerson', secondary='chem_scan_hs_resp_position')


t_chem_scan_hs_r_rate = Table(
    'chem_scan_hs_r_rate', metadata,
    Column('hs_id', ForeignKey('chem_scan_hs.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('r_rate_id', ForeignKey('chem_scan_r_rate.id'), nullable=False, index=True)
)


t_chem_scan_hs_resp_position = Table(
    'chem_scan_hs_resp_position', metadata,
    Column('hs_organization_id', ForeignKey('chem_scan_hs_organization.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('position_person_id', ForeignKey('chem_scan_position_person.id'), index=True)
)


t_chem_scan_hs_sp_rate = Table(
    'chem_scan_hs_sp_rate', metadata,
    Column('hs_id', ForeignKey('chem_scan_hs.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('sp_rate_id', ForeignKey('chem_scan_sp_rate.id'), nullable=False, index=True)
)


class ChemScanHsStock(Base):
    __tablename__ = 'chem_scan_hs_stock'

    id = Column(Integer, primary_key=True)
    hs_organization_id = Column(ForeignKey('chem_scan_hs_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    stock_id = Column(ForeignKey('chem_scan_stock.id', ondelete='CASCADE'), nullable=False, index=True)
    qty = Column(Numeric(10, 2), nullable=False)
    unit = Column(String(30, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    hs_organization = relationship('ChemScanHsOrganization')
    stock = relationship('ChemScanStock')


class ChemScanHsSubstance(Base):
    __tablename__ = 'chem_scan_hs_substance'

    id = Column(Integer, primary_key=True)
    substance_id = Column(ForeignKey('chem_scan_substance.id'), nullable=False, index=True)
    hs_id = Column(ForeignKey('chem_scan_hs.id', ondelete='CASCADE'), nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    hs = relationship('ChemScanH')
    substance = relationship('ChemScanSubstance')


class ChemScanHsSubstitute(Base):
    __tablename__ = 'chem_scan_hs_substitute'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    hs_id = Column(ForeignKey('chem_scan_hs.id', ondelete='CASCADE'), nullable=False, index=True)
    hs_usage_id = Column(ForeignKey('chem_scan_hs_usage.id', ondelete='CASCADE'), nullable=False, index=True)
    hs_substitution_id = Column(ForeignKey('chem_scan_hs_substitution.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    hs = relationship('ChemScanH')
    hs_substitution = relationship('ChemScanHsSubstitution')
    hs_usage = relationship('ChemScanHsUsage')
    organization = relationship('OroOrganization')


class ChemScanHsSubstitution(Base):
    __tablename__ = 'chem_scan_hs_substitution'

    id = Column(Integer, primary_key=True)
    hs_id = Column(ForeignKey('chem_scan_hs.id', ondelete='CASCADE'), nullable=False, index=True)
    hs_usage_id = Column(Integer)
    hs_substitute_id = Column(ForeignKey('chem_scan_hs.id', ondelete='CASCADE'), nullable=False, index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    purpose_id = Column(ForeignKey('chem_scan_purpose.id'), nullable=False, index=True)
    material_id = Column(ForeignKey('chem_scan_material.id'), nullable=False, index=True)
    procedure_id = Column(ForeignKey('chem_scan_procedure.id'), nullable=False, index=True)
    proc_id = Column(ForeignKey('chem_scan_proc.id'), index=True)
    qty = Column(String(30, 'utf8_unicode_ci'), nullable=False)
    excrete = Column(String(30, 'utf8_unicode_ci'), nullable=False)
    frequency = Column(String(30, 'utf8_unicode_ci'), nullable=False)
    surface = Column(String(30, 'utf8_unicode_ci'), nullable=False)
    duration = Column(String(30, 'utf8_unicode_ci'), nullable=False)
    air_supply = Column(String(30, 'utf8_unicode_ci'), nullable=False)
    sds_revision = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    suitable = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    health_reason = Column(String(collation='utf8_unicode_ci'))
    economy_reason = Column(String(collation='utf8_unicode_ci'))
    env_reason = Column(String(collation='utf8_unicode_ci'))
    technical_reason = Column(String(collation='utf8_unicode_ci'))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    hs_data = Column(String(collation='utf8_unicode_ci'), nullable=False)
    hs_substitute_data = Column(String(collation='utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    hs = relationship('ChemScanH', primaryjoin='ChemScanHsSubstitution.hs_id == ChemScanH.id')
    hs_substitute = relationship('ChemScanH', primaryjoin='ChemScanHsSubstitution.hs_substitute_id == ChemScanH.id')
    material = relationship('ChemScanMaterial')
    organization = relationship('OroOrganization')
    proc = relationship('ChemScanProc')
    procedure = relationship('ChemScanProcedure')
    purpose = relationship('ChemScanPurpose')


t_chem_scan_hs_symbol = Table(
    'chem_scan_hs_symbol', metadata,
    Column('symbol_id', ForeignKey('chem_scan_symbol.id'), nullable=False, index=True),
    Column('hs_id', ForeignKey('chem_scan_hs.id', ondelete='CASCADE'), nullable=False, index=True)
)


class ChemScanHsUsage(Base):
    __tablename__ = 'chem_scan_hs_usage'

    id = Column(Integer, primary_key=True)
    hs_organization_id = Column(ForeignKey('chem_scan_hs_organization.id'), nullable=False, index=True)
    scope_id = Column(ForeignKey('chem_scan_scope.id'), nullable=False, index=True)
    proc_id = Column(ForeignKey('chem_scan_proc.id'), index=True)
    user_defined_procedure_id = Column(ForeignKey('chem_scan_ud_procedure.id', ondelete='SET NULL'), index=True)
    purpose_id = Column(ForeignKey('chem_scan_purpose.id'), nullable=False, index=True)
    material_id = Column(ForeignKey('chem_scan_material.id'), nullable=False, index=True)
    procedure_id = Column(ForeignKey('chem_scan_procedure.id'), index=True)
    qty = Column(Integer, nullable=False)
    excrete = Column(Integer, nullable=False)
    frequency = Column(Integer, nullable=False)
    surface = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    air_supply = Column(Integer, nullable=False)
    flammable = Column(SmallInteger)
    closed_system = Column(SmallInteger)
    dusting = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    hs_organization = relationship('ChemScanHsOrganization')
    material = relationship('ChemScanMaterial')
    proc = relationship('ChemScanProc')
    procedure = relationship('ChemScanProcedure')
    purpose = relationship('ChemScanPurpose')
    scope = relationship('ChemScanScope')
    user_defined_procedure = relationship('ChemScanUdProcedure')
    usage_plant = relationship("ChemScanHsUsagePlant", back_populates="hs_usages")



class ChemScanHsUsagePlant(Base):
    __tablename__ = 'chem_scan_hs_usage_plant'
    __table_args__ = (
        Index('UNIQ_121983CE75774F5E1D935652', 'hs_usage_id', 'plant_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    hs_usage_id = Column(ForeignKey('chem_scan_hs_usage.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
    plant_id = Column(ForeignKey('chem_scan_plant.id', ondelete='CASCADE'),primary_key=True,  nullable=False, index=True)
    qty = Column(Numeric(10, 2))
    unit = Column(String(30, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    hs_usages = relationship("ChemScanHsUsage", back_populates="usage_plant")
    plants = relationship("ChemScanPlant", back_populates="plant_usage")


class ChemScanHsUsageRating(Base):
    __tablename__ = 'chem_scan_hs_usage_rating'

    id = Column(Integer, primary_key=True)
    hs_usage_id = Column(ForeignKey('chem_scan_hs_usage.id', ondelete='CASCADE'), nullable=False, index=True)
    breathe_emkg_id = Column(ForeignKey('chem_scan_breathe_emkg.id', ondelete='CASCADE'), index=True)
    skin_emkg_id = Column(ForeignKey('chem_scan_skin_emkg.id', ondelete='CASCADE'), index=True)
    fire_emkg_id = Column(ForeignKey('chem_scan_fire_emkg.id', ondelete='CASCADE'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    breathe_emkg = relationship('ChemScanBreatheEmkg')
    fire_emkg = relationship('ChemScanFireEmkg')
    hs_usage = relationship('ChemScanHsUsage')
    skin_emkg = relationship('ChemScanSkinEmkg')


class ChemScanKmr(Base):
    __tablename__ = 'chem_scan_kmr'

    id = Column(Integer, primary_key=True)
    new = Column(SmallInteger)
    cas = Column(String(255, 'utf8_unicode_ci'))
    eg = Column(String(255, 'utf8_unicode_ci'))
    k = Column(String(255, 'utf8_unicode_ci'))
    m = Column(String(255, 'utf8_unicode_ci'))
    rd = Column(String(255, 'utf8_unicode_ci'))
    rf = Column(String(255, 'utf8_unicode_ci'))
    date = Column(Date)
    kmr_property = Column(String(collation='utf8_unicode_ci'))
    examination = Column(String(255, 'utf8_unicode_ci'))
    regulation = Column(String(255, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanLagerClas(Base):
    __tablename__ = 'chem_scan_lager_class'

    id = Column(Integer, primary_key=True)
    _class = Column('class', String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    assesment = Column(Numeric(10, 4), nullable=False)
    zerosum = Column(String(255, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanLagerClassRule(Base):
    __tablename__ = 'chem_scan_lager_class_rule'

    id = Column(Integer, primary_key=True)
    lager_class_id = Column(ForeignKey('chem_scan_lager_class.id'), nullable=False, index=True)
    r_rate_id = Column(ForeignKey('chem_scan_r_rate.id'), index=True)
    hazard_note_id = Column(ForeignKey('chem_scan_hazard_note.id'), index=True)
    packing_group_id = Column(ForeignKey('chem_scan_packing_group.id'), index=True)
    un_number_id = Column(ForeignKey('chem_scan_un_number.id'), index=True)
    form = Column(String(255, 'utf8_unicode_ci'))
    flammable = Column(SmallInteger)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    hazard_note = relationship('ChemScanHazardNote')
    lager_class = relationship('ChemScanLagerClas')
    packing_group = relationship('ChemScanPackingGroup')
    r_rate = relationship('ChemScanRRate')
    un_number = relationship('ChemScanUnNumber')


class ChemScanManSupplier(Base):
    __tablename__ = 'chem_scan_man_supplier'

    id = Column(Integer, primary_key=True)
    company_name = Column(String(255, 'utf8_unicode_ci'))
    address = Column(String(255, 'utf8_unicode_ci'))
    zip = Column(String(255, 'utf8_unicode_ci'))
    city = Column(String(255, 'utf8_unicode_ci'))
    phone = Column(String(255, 'utf8_unicode_ci'))
    fax = Column(String(255, 'utf8_unicode_ci'))
    email = Column(String(255, 'utf8_unicode_ci'))
    location = Column(String(255, 'utf8_unicode_ci'))
    department = Column(String(255, 'utf8_unicode_ci'))
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanMaterial(Base):
    __tablename__ = 'chem_scan_material'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanNew(Base):
    __tablename__ = 'chem_scan_news'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    subject = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    text = Column(String(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')


class ChemScanOrganizationScope(Base):
    __tablename__ = 'chem_scan_organization_scope'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    organization_scope_id = Column(ForeignKey('chem_scan_organization_scope.id', ondelete='SET NULL'), index=True)
    position_person_id = Column(ForeignKey('chem_scan_position_person.id'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(collation='utf8_unicode_ci'))
    address = Column(String(collation='utf8_unicode_ci'))
    zip = Column(String(collation='utf8_unicode_ci'))
    city = Column(String(collation='utf8_unicode_ci'))
    country_id = Column(String(collation='utf8_unicode_ci'))
    fax = Column(String(collation='utf8_unicode_ci'))
    phone = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')
    organization_scope = relationship('ChemScanOrganizationScope', remote_side=[id])
    position_person = relationship('ChemScanPositionPerson')


class ChemScanOrganizationUnit(Base):
    __tablename__ = 'chem_scan_organization_unit'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    organization_unit_id = Column(ForeignKey('chem_scan_organization_unit.id'), index=True)
    organization_scope_id = Column(ForeignKey('chem_scan_organization_scope.id', ondelete='SET NULL'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    address = Column(Text(collation='utf8_unicode_ci'))
    zip = Column(String(255, 'utf8_unicode_ci'))
    city = Column(String(255, 'utf8_unicode_ci'))
    country_id = Column(ForeignKey('oro_dictionary_country.iso2_code'), index=True)
    fax = Column(String(255, 'utf8_unicode_ci'))
    phone = Column(String(255, 'utf8_unicode_ci'))
    description = Column(String(collation='utf8_unicode_ci'))
    position_person_id = Column(ForeignKey('chem_scan_position_person.id', ondelete='SET NULL'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    country = relationship('OroDictionaryCountry')
    organization = relationship('OroOrganization')
    organization_scope = relationship('ChemScanOrganizationScope')
    organization_unit = relationship('ChemScanOrganizationUnit', remote_side=[id])
    position_person = relationship('ChemScanPositionPerson')


class ChemScanOwnCatalog(Base):
    __tablename__ = 'chem_scan_own_catalog'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    code = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    protection_action = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')


class ChemScanOwnCatalogSubst(Base):
    __tablename__ = 'chem_scan_own_catalog_subst'

    id = Column(Integer, primary_key=True)
    own_catalog_id = Column(ForeignKey('chem_scan_own_catalog.id', ondelete='CASCADE'), nullable=False, index=True)
    substance_id = Column(ForeignKey('chem_scan_substance.id', ondelete='CASCADE'), nullable=False, index=True)
    additional_1 = Column(String(collation='utf8_unicode_ci'))
    additional_2 = Column(String(collation='utf8_unicode_ci'))
    additional_3 = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    own_catalog = relationship('ChemScanOwnCatalog')
    substance = relationship('ChemScanSubstance')


class ChemScanPa(Base):
    __tablename__ = 'chem_scan_pa'

    id = Column(Integer, primary_key=True)
    pa_group_id = Column(ForeignKey('chem_scan_pa_group.id', ondelete='SET NULL'), index=True)
    pa_source_chapter_id = Column(ForeignKey('chem_scan_pa_source_chapter.id', ondelete='SET NULL'), index=True)
    type = Column(String(255, 'utf8_unicode_ci'))
    show_always = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    operation_instruction = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    technical = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    personal = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    organizational = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    text = Column(String(collation='utf8_unicode_ci'), nullable=False)
    up_to_date = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    update_date = Column(Date)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    pa_group = relationship('ChemScanPaGroup')
    pa_source_chapter = relationship('ChemScanPaSourceChapter')


class ChemScanPaGroup(Base):
    __tablename__ = 'chem_scan_pa_group'

    id = Column(Integer, primary_key=True)
    text = Column(String(collation='utf8_unicode_ci'), nullable=False)

    operation_instruction = Column(SmallInteger, server_default=raw_text("0"))

    organizational = Column(SmallInteger, server_default=raw_text("0"))
    personal = Column(SmallInteger, server_default=raw_text("0"))
    technical = Column(SmallInteger, server_default=raw_text("0"))
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanPaLevel(Base):
    __tablename__ = 'chem_scan_pa_level'

    id = Column(Integer, primary_key=True)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)


t_chem_scan_pa_rate_bemkg = Table(
    'chem_scan_pa_rate_bemkg', metadata,
    Column('pa_id', ForeignKey('chem_scan_pa.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('rating', SmallInteger, nullable=False)
)


t_chem_scan_pa_rate_femkg = Table(
    'chem_scan_pa_rate_femkg', metadata,
    Column('pa_id', ForeignKey('chem_scan_pa.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('rating', SmallInteger, nullable=False)
)


t_chem_scan_pa_rate_semkg = Table(
    'chem_scan_pa_rate_semkg', metadata,
    Column('pa_id', ForeignKey('chem_scan_pa.id', ondelete='CASCADE'), nullable=False, index=True),
    Column('rating', SmallInteger, nullable=False)
)


class ChemScanPaSource(Base):
    __tablename__ = 'chem_scan_pa_source'

    id = Column(Integer, primary_key=True)
    pa_level_id = Column(ForeignKey('chem_scan_pa_level.id', ondelete='CASCADE'), nullable=False, index=True)
    code = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    pa_level = relationship('ChemScanPaLevel')


class ChemScanPaSourceChapter(Base):
    __tablename__ = 'chem_scan_pa_source_chapter'

    id = Column(Integer, primary_key=True)
    pa_source_id = Column(ForeignKey('chem_scan_pa_source.id', ondelete='CASCADE'), nullable=False, index=True)
    title = Column(String(225, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    pa_source = relationship('ChemScanPaSource')


class ChemScanPaSourceRuleBemkg(Base):
    __tablename__ = 'chem_scan_pa_source_rule_bemkg'

    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    qg = Column(Integer, nullable=False)
    eg = Column(Integer, nullable=False)
    pa_source_code = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    rule = Column(String(collation='utf8_unicode_ci'))


class ChemScanPaSourceRuleFemkg(Base):
    __tablename__ = 'chem_scan_pa_source_rule_femkg'

    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    qg = Column(Integer, nullable=False)
    eg = Column(Integer, nullable=False)
    pa_source_code = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    rule = Column(String(collation='utf8_unicode_ci'))


class ChemScanPaSourceRuleSemkg(Base):
    __tablename__ = 'chem_scan_pa_source_rule_semkg'

    id = Column(Integer, primary_key=True)
    rating = Column(Integer, nullable=False)
    sg = Column(Integer, nullable=False)
    dg = Column(Integer, nullable=False)
    pa_source_code = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    rule = Column(String(collation='utf8_unicode_ci'))


class ChemScanPackingGroup(Base):
    __tablename__ = 'chem_scan_packing_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanPerson(Base):
    __tablename__ = 'chem_scan_person'
    __table_args__ = (
        Index('IDX_FD212039A9D1C132C808BA5A', 'first_name', 'last_name'),
    )

    id = Column(Integer, primary_key=True)
    person_group_id = Column(ForeignKey('chem_scan_person_group.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    title = Column(String(255, 'utf8_unicode_ci'))
    first_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    last_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    gender = Column(String(255, 'utf8_unicode_ci'))
    dob = Column(Date, index=True)
    email = Column(String(255, 'utf8_unicode_ci'), index=True)
    profession = Column(String(255, 'utf8_unicode_ci'))
    status = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    hire_date = Column(Date)
    fire_date = Column(Date)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')
    person_group = relationship('ChemScanPersonGroup')


class ChemScanPersonGroup(Base):
    __tablename__ = 'chem_scan_person_group'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')


class ChemScanPictogramEscape(Base):
    __tablename__ = 'chem_scan_pictogram_escape'

    id = Column(Integer, primary_key=True)
    image_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    oi_default = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    image = relationship('OroAttachmentFile')


class ChemScanPictogramFire(Base):
    __tablename__ = 'chem_scan_pictogram_fire'

    id = Column(Integer, primary_key=True)
    image_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    oi_default = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    image = relationship('OroAttachmentFile')


class ChemScanPictogramOffer(Base):
    __tablename__ = 'chem_scan_pictogram_offer'

    id = Column(Integer, primary_key=True)
    image_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    oi_default = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    image = relationship('OroAttachmentFile')


class ChemScanPictogramProh(Base):
    __tablename__ = 'chem_scan_pictogram_proh'

    id = Column(Integer, primary_key=True)
    image_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    oi_default = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    image = relationship('OroAttachmentFile')


class ChemScanPictogramWarn(Base):
    __tablename__ = 'chem_scan_pictogram_warn'

    id = Column(Integer, primary_key=True)
    image_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    oi_default = Column(SmallInteger, nullable=False, server_default=raw_text("0"))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    image = relationship('OroAttachmentFile')


class ChemScanPlant(Base):
    __tablename__ = 'chem_scan_plant'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    organization_unit_id = Column(ForeignKey('chem_scan_organization_unit.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    organization_scope_id = Column(ForeignKey('chem_scan_organization_scope.id', ondelete='SET NULL'), index=True)
    plant_type_id = Column(ForeignKey('chem_scan_plant_type.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    abbr = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(collation='utf8_unicode_ci'))
    volume = Column(Numeric(10, 4))
    unit = Column(String(30, 'utf8_unicode_ci'))
    whc = Column(Integer, nullable=False, server_default=raw_text("0"))
    position_person_id = Column(ForeignKey('chem_scan_position_person.id'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')
    organization_scope = relationship('ChemScanOrganizationScope')
    organization_unit = relationship('ChemScanOrganizationUnit')
    plant_type = relationship('ChemScanPlantType')
    position_person = relationship('ChemScanPositionPerson')
    plant_usage = relationship("ChemScanHsUsagePlant", back_populates='plants')
    orga = relationship("OroOrganization", back_populates="plant")

class ChemScanPlantCalculation(Base):
    __tablename__ = 'chem_scan_plant_calculation'

    id = Column(Integer, primary_key=True)
    plant_id = Column(ForeignKey('chem_scan_plant.id', ondelete='CASCADE'), nullable=False, index=True)
    whc = Column(Integer, nullable=False, server_default=raw_text("0"))

    plant = relationship('ChemScanPlant')


class ChemScanPlantType(Base):
    __tablename__ = 'chem_scan_plant_type'

    id = Column(Integer, primary_key=True)
    plant_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)


class ChemScanPosition(Base):
    __tablename__ = 'chem_scan_position'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')


class ChemScanPositionPerson(Base):
    __tablename__ = 'chem_scan_position_person'

    id = Column(Integer, primary_key=True)
    person_id = Column(ForeignKey('chem_scan_person.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    position_id = Column(ForeignKey('chem_scan_position.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    document_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    document = relationship('OroAttachmentFile')
    organization = relationship('OroOrganization')
    person = relationship('ChemScanPerson')
    position = relationship('ChemScanPosition')


class ChemScanProc(Base):
    __tablename__ = 'chem_scan_proc'

    id = Column(Integer, primary_key=True)
    proc = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(collation='utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanProcedure(Base):
    __tablename__ = 'chem_scan_procedure'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanPurpose(Base):
    __tablename__ = 'chem_scan_purpose'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanRRate(Base):
    __tablename__ = 'chem_scan_r_rate'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(collation='utf8_unicode_ci'), nullable=False)
    breathe_emkg_hazard_group = Column(Integer)
    skin_emkg_hazard_group = Column(Integer)
    fire_emkg_hazard_group = Column(Integer)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    w_factor = Column(Integer)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanReach14(Base):
    __tablename__ = 'chem_scan_reach14'

    id = Column(Integer, primary_key=True)
    cas = Column(String(255, 'utf8_unicode_ci'))
    eg = Column(String(255, 'utf8_unicode_ci'))
    property = Column(String(255, 'utf8_unicode_ci'))
    approval_from = Column(Date)
    approval_till = Column(Date)
    comment = Column(String(collation='utf8_unicode_ci'))
    date = Column(Date)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanReach17(Base):
    __tablename__ = 'chem_scan_reach17'

    id = Column(Integer, primary_key=True)
    cas = Column(String(255, 'utf8_unicode_ci'))
    eg = Column(String(255, 'utf8_unicode_ci'))
    comment = Column(String(collation='utf8_unicode_ci'))
    reach_group = Column(String(255, 'utf8_unicode_ci'))
    substance = Column(String(255, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanReadNew(Base):
    __tablename__ = 'chem_scan_read_news'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id'), nullable=False, index=True)
    news_id = Column(ForeignKey('chem_scan_news.id'), nullable=False, index=True)

    news = relationship('ChemScanNew')
    user = relationship('OroUser')


class ChemScanReason(Base):
    __tablename__ = 'chem_scan_reason'

    id = Column(Integer, primary_key=True)
    question = Column(String(collation='utf8_unicode_ci'))
    type = Column(String(255, 'utf8_unicode_ci'))


class ChemScanSafetyDatasheet(Base):
    __tablename__ = 'chem_scan_safety_datasheet'

    id = Column(Integer, primary_key=True)
    hs_id = Column(ForeignKey('chem_scan_hs.id'), nullable=False, index=True)
    document_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    revision = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    type = Column(String(255, 'utf8_unicode_ci'))
    printed = Column(Date)
    updated = Column(Date)
    approved = Column(SmallInteger, nullable=False)
    checked = Column(Date)
    reasonable = Column(SmallInteger)
    statement = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    document = relationship('OroAttachmentFile')
    hs = relationship('ChemScanH')


class ChemScanScope(Base):
    __tablename__ = 'chem_scan_scope'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    area = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(255, 'utf8_unicode_ci'))
    position_person_id = Column(ForeignKey('chem_scan_position_person.id', ondelete='CASCADE'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')
    position_person = relationship('ChemScanPositionPerson')


class ChemScanSen(Base):
    __tablename__ = 'chem_scan_sens'

    id = Column(Integer, primary_key=True)
    symbol_id = Column(ForeignKey('chem_scan_symbol.id'), index=True)
    r_rate_id = Column(ForeignKey('chem_scan_r_rate.id'), index=True)
    eg = Column(String(255, 'utf8_unicode_ci'))
    cas = Column(String(255, 'utf8_unicode_ci'))
    date = Column(Date)
    vo = Column(String(255, 'utf8_unicode_ci'))
    specificity = Column(String(255, 'utf8_unicode_ci'))
    examination = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    r_rate = relationship('ChemScanRRate')
    symbol = relationship('ChemScanSymbol')


class ChemScanServiceRequest(Base):
    __tablename__ = 'chem_scan_service_request'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id'), nullable=False, index=True)
    subject = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    text = Column(String(collation='utf8_unicode_ci'), nullable=False)
    is_read = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime, nullable=False)

    user = relationship('OroUser')


class ChemScanSkinEmkg(Base):
    __tablename__ = 'chem_scan_skin_emkg'

    id = Column(Integer, primary_key=True)
    code = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    hg = Column(SmallInteger, nullable=False)
    sg = Column(SmallInteger, nullable=False)
    dg = Column(SmallInteger, nullable=False)
    rating = Column(SmallInteger, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanSkinEmkgRule(Base):
    __tablename__ = 'chem_scan_skin_emkg_rule'

    id = Column(Integer, primary_key=True)
    skin_emkg_rating = Column(SmallInteger, nullable=False)
    rule = Column(String(collation='utf8_unicode_ci'), nullable=False)


class ChemScanSpRate(Base):
    __tablename__ = 'chem_scan_sp_rate'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(collation='utf8_unicode_ci'), nullable=False)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanStock(Base):
    __tablename__ = 'chem_scan_stock'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    organization_unit_id = Column(ForeignKey('chem_scan_organization_unit.id', ondelete='SET NULL', onupdate='CASCADE'), index=True)
    organization_scope_id = Column(ForeignKey('chem_scan_organization_scope.id', ondelete='SET NULL'), index=True)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    ventilation_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    surface = Column(Numeric(10, 2))
    height = Column(Numeric(10, 2))
    air_supply = Column(Numeric(10, 2))
    ventilation_rate = Column(Numeric(10, 0), nullable=False)
    description = Column(String(255, 'utf8_unicode_ci'))
    position_person_id = Column(ForeignKey('chem_scan_position_person.id', ondelete='CASCADE'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')
    organization_scope = relationship('ChemScanOrganizationScope')
    organization_unit = relationship('ChemScanOrganizationUnit')
    position_person = relationship('ChemScanPositionPerson')


class ChemScanStockRule(Base):
    __tablename__ = 'chem_scan_stock_rule'

    id = Column(Integer, primary_key=True)
    stock_rule_cipher_id = Column(ForeignKey('chem_scan_stock_rule_cipher.id'), index=True)
    lager_class_id_1 = Column(ForeignKey('chem_scan_lager_class.id'), nullable=False, index=True)
    lager_class_id_2 = Column(ForeignKey('chem_scan_lager_class.id'), nullable=False, index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    chem_scan_lager_clas = relationship('ChemScanLagerClas', primaryjoin='ChemScanStockRule.lager_class_id_1 == ChemScanLagerClas.id')
    chem_scan_lager_clas1 = relationship('ChemScanLagerClas', primaryjoin='ChemScanStockRule.lager_class_id_2 == ChemScanLagerClas.id')
    stock_rule_cipher = relationship('ChemScanStockRuleCipher')


class ChemScanStockRuleCipher(Base):
    __tablename__ = 'chem_scan_stock_rule_cipher'

    id = Column(Integer, primary_key=True)
    cipher = Column(String(5, 'utf8_unicode_ci'), nullable=False)
    text = Column(String(collation='utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanSubstance(Base):
    __tablename__ = 'chem_scan_substance'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'))
    eg = Column(String(255, 'utf8_unicode_ci'))
    cas = Column(String(255, 'utf8_unicode_ci'))
    reach_nr = Column(String(255, 'utf8_unicode_ci'))
    formula = Column(String(collation='utf8_unicode_ci'))
    approved = Column(SmallInteger)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanSubstanceGroup(Base):
    __tablename__ = 'chem_scan_substance_group'

    id = Column(Integer, primary_key=True)
    code = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    description = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanSubstanceWhc(Base):
    __tablename__ = 'chem_scan_substance_whc'

    id = Column(Integer, primary_key=True)
    cas = Column(String(255, 'utf8_unicode_ci'))
    ex_sign = Column(String(255, 'utf8_unicode_ci'))
    ex_status = Column(String(255, 'utf8_unicode_ci'))
    _class = Column('class', Integer)
    rating = Column(String(255, 'utf8_unicode_ci'))
    rating_date = Column(Date)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanSymbol(Base):
    __tablename__ = 'chem_scan_symbol'

    id = Column(Integer, primary_key=True)
    image_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    sign = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    new = Column(SmallInteger, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    image = relationship('OroAttachmentFile')


class ChemScanTrgs910(Base):
    __tablename__ = 'chem_scan_trgs910'

    id = Column(Integer, primary_key=True)
    eg = Column(String(255, 'utf8_unicode_ci'))
    cas = Column(String(255, 'utf8_unicode_ci'))
    air_acceptance = Column(String(255, 'utf8_unicode_ci'))
    air_tolerance = Column(String(255, 'utf8_unicode_ci'))
    overrun_factor = Column(String(255, 'utf8_unicode_ci'))
    bgw_parameter = Column(String(255, 'utf8_unicode_ci'))
    bgw_acceptance = Column(String(255, 'utf8_unicode_ci'))
    bgw_tolerance = Column(String(255, 'utf8_unicode_ci'))
    comment = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanUdProcedure(Base):
    __tablename__ = 'chem_scan_ud_procedure'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')


class ChemScanUnNumber(Base):
    __tablename__ = 'chem_scan_un_number'

    id = Column(Integer, primary_key=True)
    un_number = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanWasteKey(Base):
    __tablename__ = 'chem_scan_waste_key'

    id = Column(Integer, primary_key=True)
    waste_key = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(collation='utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class ChemScanWhcRule(Base):
    __tablename__ = 'chem_scan_whc_rule'

    id = Column(Integer, primary_key=True)
    r_rate_id = Column(ForeignKey('chem_scan_r_rate.id'), index=True)
    _class = Column('class', Integer, nullable=False)
    class_contents = Column(SmallInteger, nullable=False)
    amount_min = Column(Numeric(10, 2))
    amount_max = Column(Numeric(10, 2))
    aggregate = Column(Integer)

    r_rate = relationship('ChemScanRRate')


class OroAccessGroup(Base):
    __tablename__ = 'oro_access_group'
    __table_args__ = (
        Index('uq_name_org_idx', 'name', 'organization_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    business_unit_owner_id = Column(ForeignKey('oro_business_unit.id', ondelete='SET NULL'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    name = Column(String(30, 'utf8_unicode_ci'), nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    business_unit_owner = relationship('OroBusinessUnit')
    organization = relationship('OroOrganization')
    recipient_lists = relationship('OroNotificationRecipList', secondary='oro_notification_recip_group')
    users = relationship('OroUser', secondary='oro_user_access_group')
    roles = relationship('OroAccessRole', secondary='oro_user_access_group_role')


class OroAccessRole(Base):
    __tablename__ = 'oro_access_role'

    id = Column(Integer, primary_key=True)
    role = Column(String(30, 'utf8_unicode_ci'), nullable=False, unique=True)
    label = Column(String(30, 'utf8_unicode_ci'), nullable=False)
    extend_description = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    users = relationship('OroUser', secondary='oro_user_access_role')


class OroActivityList(Base):
    __tablename__ = 'oro_activity_list'

    id = Column(Integer, primary_key=True)
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    user_editor_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    verb = Column(String(32, 'utf8_unicode_ci'), nullable=False)
    subject = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    related_activity_class = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    related_activity_id = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False, index=True)
    is_head = Column(Integer, nullable=False, index=True, server_default=raw_text("1"))
    description = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')
    user_editor = relationship('OroUser', primaryjoin='OroActivityList.user_editor_id == OroUser.id')
    user_owner = relationship('OroUser', primaryjoin='OroActivityList.user_owner_id == OroUser.id')
    users = relationship('OroUser', secondary='oro_rel_c3990ba62da17977270bd6')


class OroActivityOwner(Base):
    __tablename__ = 'oro_activity_owner'
    __table_args__ = (
        Index('UNQ_activity_owner', 'activity_id', 'user_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id'), index=True)
    activity_id = Column(ForeignKey('oro_activity_list.id', ondelete='CASCADE'), index=True)

    activity = relationship('OroActivityList')
    organization = relationship('OroOrganization')
    user = relationship('OroUser')


class OroAddres(Base):
    __tablename__ = 'oro_address'

    id = Column(Integer, primary_key=True)
    country_code = Column(ForeignKey('oro_dictionary_country.iso2_code'), index=True)
    region_code = Column(ForeignKey('oro_dictionary_region.combined_code'), index=True)
    label = Column(String(255, 'utf8_unicode_ci'))
    street = Column(String(500, 'utf8_unicode_ci'))
    street2 = Column(String(500, 'utf8_unicode_ci'))
    city = Column(String(255, 'utf8_unicode_ci'))
    postal_code = Column(String(255, 'utf8_unicode_ci'))
    organization = Column(String(255, 'utf8_unicode_ci'))
    region_text = Column(String(255, 'utf8_unicode_ci'))
    name_prefix = Column(String(255, 'utf8_unicode_ci'))
    first_name = Column(String(255, 'utf8_unicode_ci'))
    middle_name = Column(String(255, 'utf8_unicode_ci'))
    last_name = Column(String(255, 'utf8_unicode_ci'))
    name_suffix = Column(String(255, 'utf8_unicode_ci'))
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    oro_dictionary_country = relationship('OroDictionaryCountry')
    oro_dictionary_region = relationship('OroDictionaryRegion')


class OroAddressType(Base):
    __tablename__ = 'oro_address_type'

    name = Column(String(16, 'utf8_unicode_ci'), primary_key=True)
    label = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)


class OroAddressTypeTranslation(Base):
    __tablename__ = 'oro_address_type_translation'
    __table_args__ = (
        Index('address_type_translation_idx', 'locale', 'object_class', 'field', 'foreign_key'),
    )

    id = Column(Integer, primary_key=True)
    foreign_key = Column(String(16, 'utf8_unicode_ci'), nullable=False)
    content = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    locale = Column(String(8, 'utf8_unicode_ci'), nullable=False)
    object_class = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    field = Column(String(32, 'utf8_unicode_ci'), nullable=False)


class OroAttachment(Base):
    __tablename__ = 'oro_attachment'

    id = Column(Integer, primary_key=True)
    file_id = Column(ForeignKey('oro_attachment_file.id'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    comment = Column(String(collation='utf8_unicode_ci'))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    owner_user_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    position_person_8b30121b_id = Column(ForeignKey('chem_scan_position_person.id', ondelete='SET NULL'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    file = relationship('OroAttachmentFile')
    organization = relationship('OroOrganization')
    owner_user = relationship('OroUser')
    position_person_8b30121b = relationship('ChemScanPositionPerson')


class OroAttachmentFile(Base):
    __tablename__ = 'oro_attachment_file'

    id = Column(Integer, primary_key=True)
    filename = Column(String(255, 'utf8_unicode_ci'))
    extension = Column(String(10, 'utf8_unicode_ci'))
    mime_type = Column(String(100, 'utf8_unicode_ci'))
    file_size = Column(Integer)
    original_filename = Column(String(255, 'utf8_unicode_ci'), index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    owner_user_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    owner_user = relationship('OroUser', primaryjoin='OroAttachmentFile.owner_user_id == OroUser.id')


class OroAttributeFamily(Base):
    __tablename__ = 'oro_attribute_family'

    id = Column(Integer, primary_key=True)
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    image_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    code = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    entity_class = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    is_enabled = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    image = relationship('OroAttachmentFile')
    organization = relationship('OroOrganization')
    user_owner = relationship('OroUser')
    localized_values = relationship('OroFallbackLocalizationVal', secondary='oro_attribute_family_label')


t_oro_attribute_family_label = Table(
    'oro_attribute_family_label', metadata,
    Column('attribute_family_id', ForeignKey('oro_attribute_family.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('localized_value_id', ForeignKey('oro_fallback_localization_val.id', ondelete='CASCADE'), primary_key=True, nullable=False, unique=True)
)


class OroAttributeGroup(Base):
    __tablename__ = 'oro_attribute_group'

    id = Column(Integer, primary_key=True)
    attribute_family_id = Column(ForeignKey('oro_attribute_family.id'), index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    code = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    is_visible = Column(Integer, nullable=False, server_default=raw_text("1"))

    attribute_family = relationship('OroAttributeFamily')
    localized_values = relationship('OroFallbackLocalizationVal', secondary='oro_attribute_group_label')


t_oro_attribute_group_label = Table(
    'oro_attribute_group_label', metadata,
    Column('attribute_group_id', ForeignKey('oro_attribute_group.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('localized_value_id', ForeignKey('oro_fallback_localization_val.id', ondelete='CASCADE'), primary_key=True, nullable=False, unique=True)
)


class OroAttributeGroupRel(Base):
    __tablename__ = 'oro_attribute_group_rel'
    __table_args__ = (
        Index('oro_attribute_group_uidx', 'entity_config_field_id', 'attribute_group_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    attribute_group_id = Column(ForeignKey('oro_attribute_group.id'), index=True)
    entity_config_field_id = Column(Integer, nullable=False)

    attribute_group = relationship('OroAttributeGroup')


class OroAudit(Base):
    __tablename__ = 'oro_audit'
    __table_args__ = (
        Index('idx_oro_audit_version', 'object_id', 'object_class', 'version', unique=True),
        Index('idx_oro_audit_obj_by_type', 'object_id', 'object_class', 'type')
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    action = Column(String(8, 'utf8_unicode_ci'))
    logged_at = Column(DateTime, index=True)
    object_id = Column(Integer)
    object_class = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    object_name = Column(String(255, 'utf8_unicode_ci'))
    version = Column(Integer)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    transaction_id = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    impersonation_id = Column(ForeignKey('oro_user_impersonation.id', ondelete='SET NULL'), index=True)
    owner_description = Column(String(255, 'utf8_unicode_ci'))

    impersonation = relationship('OroUserImpersonation')
    organization = relationship('OroOrganization')
    user = relationship('OroUser')


class OroAuditField(Base):
    __tablename__ = 'oro_audit_field'

    id = Column(Integer, primary_key=True)
    audit_id = Column(ForeignKey('oro_audit.id', ondelete='CASCADE'), nullable=False, index=True)
    field = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    data_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    old_integer = Column(BigInteger)
    old_float = Column(Float(asdecimal=True))
    old_boolean = Column(Integer)
    old_text = Column(String(collation='utf8_unicode_ci'))
    old_date = Column(Date)
    old_time = Column(Time)
    old_datetime = Column(DateTime)
    new_integer = Column(BigInteger)
    new_float = Column(Float(asdecimal=True))
    new_boolean = Column(Integer)
    new_text = Column(String(collation='utf8_unicode_ci'))
    new_date = Column(Date)
    new_time = Column(Time)
    new_datetime = Column(DateTime)
    old_datetimetz = Column(DateTime)
    old_object = Column(String(collation='utf8_unicode_ci'))
    new_datetimetz = Column(DateTime)
    new_object = Column(String(collation='utf8_unicode_ci'))
    visible = Column(Integer, nullable=False, server_default=raw_text("1"))
    old_array = Column(String(collation='utf8_unicode_ci'))
    new_array = Column(String(collation='utf8_unicode_ci'))
    old_simplearray = Column(String(collation='utf8_unicode_ci'))
    new_simplearray = Column(String(collation='utf8_unicode_ci'))
    old_jsonarray = Column(String(collation='utf8_unicode_ci'))
    new_jsonarray = Column(String(collation='utf8_unicode_ci'))
    collection_diffs = Column(String(collation='utf8_unicode_ci'))

    audit = relationship('OroAudit')


class OroBusinessUnit(Base):
    __tablename__ = 'oro_business_unit'

    id = Column(Integer, primary_key=True)
    business_unit_owner_id = Column(ForeignKey('oro_business_unit.id', ondelete='SET NULL'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), nullable=False, index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    phone = Column(String(100, 'utf8_unicode_ci'))
    website = Column(String(255, 'utf8_unicode_ci'))
    email = Column(String(255, 'utf8_unicode_ci'))
    fax = Column(String(255, 'utf8_unicode_ci'))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    extend_description = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    business_unit_owner = relationship('OroBusinessUnit', remote_side=[id])
    organization = relationship('OroOrganization')
    users = relationship('OroUser', secondary='oro_user_business_unit')


class OroCalendar(Base):
    __tablename__ = 'oro_calendar'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')
    user_owner = relationship('OroUser')


class OroCalendarDate(Base):
    __tablename__ = 'oro_calendar_date'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)


class OroCalendarEvent(Base):
    __tablename__ = 'oro_calendar_event'
    __table_args__ = (
        Index('oro_sys_calendar_event_idx', 'system_calendar_id', 'start_at', 'end_at'),
        Index('oro_calendar_event_idx', 'calendar_id', 'start_at', 'end_at')
    )

    id = Column(Integer, primary_key=True)
    calendar_id = Column(ForeignKey('oro_calendar.id', ondelete='CASCADE'), index=True)
    system_calendar_id = Column(ForeignKey('oro_system_calendar.id', ondelete='CASCADE'), index=True)
    parent_id = Column(ForeignKey('oro_calendar_event.id', ondelete='CASCADE'), index=True)
    title = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(collation='utf8_unicode_ci'))
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    all_day = Column(Integer, nullable=False)
    background_color = Column(String(7, 'utf8_unicode_ci'))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False, index=True)
    related_attendee_id = Column(ForeignKey('oro_calendar_event_attendee.id', ondelete='SET NULL'), index=True)
    recurrence_id = Column(ForeignKey('oro_calendar_recurrence.id', ondelete='SET NULL'), unique=True)
    recurring_event_id = Column(ForeignKey('oro_calendar_event.id', ondelete='CASCADE'), index=True)
    original_start_at = Column(DateTime, index=True)
    is_cancelled = Column(Integer, nullable=False, server_default=raw_text("0"))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    calendar = relationship('OroCalendar')
    parent = relationship('OroCalendarEvent', remote_side=[id], primaryjoin='OroCalendarEvent.parent_id == OroCalendarEvent.id')
    recurrence = relationship('OroCalendarRecurrence')
    recurring_event = relationship('OroCalendarEvent', remote_side=[id], primaryjoin='OroCalendarEvent.recurring_event_id == OroCalendarEvent.id')
    related_attendee = relationship('OroCalendarEventAttendee', primaryjoin='OroCalendarEvent.related_attendee_id == OroCalendarEventAttendee.id')
    system_calendar = relationship('OroSystemCalendar')


class OroCalendarEventAttendee(Base):
    __tablename__ = 'oro_calendar_event_attendee'

    id = Column(Integer, primary_key=True)
    status_id = Column(ForeignKey('oro_enum_ce_attendee_status.id', ondelete='SET NULL'), index=True)
    type_id = Column(ForeignKey('oro_enum_ce_attendee_type.id', ondelete='SET NULL'), index=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    calendar_event_id = Column(ForeignKey('oro_calendar_event.id', ondelete='CASCADE'), index=True)
    email = Column(String(255, 'utf8_unicode_ci'))
    display_name = Column(String(255, 'utf8_unicode_ci'))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    calendar_event = relationship('OroCalendarEvent', primaryjoin='OroCalendarEventAttendee.calendar_event_id == OroCalendarEvent.id')
    status = relationship('OroEnumCeAttendeeStatu')
    type = relationship('OroEnumCeAttendeeType')
    user = relationship('OroUser')


class OroCalendarProperty(Base):
    __tablename__ = 'oro_calendar_property'
    __table_args__ = (
        Index('oro_calendar_prop_uq', 'calendar_alias', 'calendar_id', 'target_calendar_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    target_calendar_id = Column(ForeignKey('oro_calendar.id', ondelete='CASCADE'), nullable=False, index=True)
    calendar_alias = Column(String(32, 'utf8_unicode_ci'), nullable=False)
    calendar_id = Column(Integer, nullable=False)
    position = Column(Integer, nullable=False, server_default=raw_text("0"))
    visible = Column(Integer, nullable=False, server_default=raw_text("1"))
    background_color = Column(String(7, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    target_calendar = relationship('OroCalendar')


class OroCalendarRecurrence(Base):
    __tablename__ = 'oro_calendar_recurrence'

    id = Column(Integer, primary_key=True)
    recurrence_type = Column(String(16, 'utf8_unicode_ci'), nullable=False)
    interval = Column(Integer, nullable=False)
    instance = Column(Integer)
    day_of_week = Column(String(collation='utf8_unicode_ci'))
    day_of_month = Column(Integer)
    month_of_year = Column(Integer)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, index=True)
    calculated_end_time = Column(DateTime, nullable=False, index=True)
    occurrences = Column(Integer)
    timezone = Column(String(255, 'utf8_unicode_ci'), nullable=False)


class OroComment(Base):
    __tablename__ = 'oro_comment'

    id = Column(Integer, primary_key=True)
    owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    updated_by_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    email_bb212599_id = Column(ForeignKey('oro_email.id', ondelete='SET NULL'), index=True)
    calendar_event_78fb52b8_id = Column(ForeignKey('oro_calendar_event.id', ondelete='SET NULL'), index=True)
    note_c0db526d_id = Column(ForeignKey('oro_note.id', ondelete='SET NULL'), index=True)
    attachment_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    message = Column(String(collation='utf8_unicode_ci'), nullable=False)
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    attachment = relationship('OroAttachmentFile')
    calendar_event_78fb52b8 = relationship('OroCalendarEvent')
    email_bb212599 = relationship('OroEmail')
    note_c0db526d = relationship('OroNote')
    organization = relationship('OroOrganization')
    owner = relationship('OroUser', primaryjoin='OroComment.owner_id == OroUser.id')
    updated_by = relationship('OroUser', primaryjoin='OroComment.updated_by_id == OroUser.id')


class OroConfig(Base):
    __tablename__ = 'oro_config'
    __table_args__ = (
        Index('CONFIG_UQ_ENTITY', 'entity', 'record_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    entity = Column(String(255, 'utf8_unicode_ci'))
    record_id = Column(Integer)


class OroConfigValue(Base):
    __tablename__ = 'oro_config_value'
    __table_args__ = (
        Index('CONFIG_VALUE_UQ_ENTITY', 'name', 'section', 'config_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    config_id = Column(ForeignKey('oro_config.id', ondelete='CASCADE'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    section = Column(String(50, 'utf8_unicode_ci'))
    text_value = Column(String(collation='utf8_unicode_ci'))
    object_value = Column(String(collation='utf8_unicode_ci'))
    array_value = Column(String(collation='utf8_unicode_ci'))
    type = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    config = relationship('OroConfig')


class OroCronSchedule(Base):
    __tablename__ = 'oro_cron_schedule'
    __table_args__ = (
        Index('UQ_COMMAND', 'command', 'args_hash', 'definition', unique=True),
    )

    id = Column(Integer, primary_key=True)
    command = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    definition = Column(String(100, 'utf8_unicode_ci'))
    args = Column(String(collation='utf8_unicode_ci'), nullable=False)
    args_hash = Column(String(32, 'utf8_unicode_ci'), nullable=False)


class OroDashboard(Base):
    __tablename__ = 'oro_dashboard'

    id = Column(Integer, primary_key=True)
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'))
    label = Column(String(255, 'utf8_unicode_ci'))
    is_default = Column(Integer, nullable=False, index=True, server_default=raw_text("0"))
    createdat = Column(DateTime, nullable=False)
    updatedat = Column(DateTime)

    organization = relationship('OroOrganization')
    user_owner = relationship('OroUser')


class OroDashboardActive(Base):
    __tablename__ = 'oro_dashboard_active'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    dashboard_id = Column(ForeignKey('oro_dashboard.id', ondelete='CASCADE'), index=True)

    dashboard = relationship('OroDashboard')
    organization = relationship('OroOrganization')
    user = relationship('OroUser')


class OroDashboardWidget(Base):
    __tablename__ = 'oro_dashboard_widget'

    id = Column(Integer, primary_key=True)
    dashboard_id = Column(ForeignKey('oro_dashboard.id', ondelete='CASCADE'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    layout_position = Column(String(collation='utf8_unicode_ci'), nullable=False)
    options = Column(String(collation='utf8_unicode_ci'))

    dashboard = relationship('OroDashboard')


class OroDashboardWidgetState(Base):
    __tablename__ = 'oro_dashboard_widget_state'

    id = Column(Integer, primary_key=True)
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), index=True)
    widget_id = Column(ForeignKey('oro_dashboard_widget.id', ondelete='CASCADE'), index=True)
    is_expanded = Column(Integer, nullable=False)

    user_owner = relationship('OroUser')
    widget = relationship('OroDashboardWidget')


class OroDictionaryCountry(Base):
    __tablename__ = 'oro_dictionary_country'

    iso2_code = Column(String(2, 'utf8_unicode_ci'), primary_key=True)
    iso3_code = Column(String(3, 'utf8_unicode_ci'), nullable=False)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))


class OroDictionaryCountryTran(Base):
    __tablename__ = 'oro_dictionary_country_trans'
    __table_args__ = (
        Index('country_translation_idx', 'locale', 'object_class', 'field', 'foreign_key'),
    )

    id = Column(Integer, primary_key=True)
    foreign_key = Column(String(2, 'utf8_unicode_ci'), nullable=False)
    content = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    locale = Column(String(8, 'utf8_unicode_ci'), nullable=False)
    object_class = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    field = Column(String(32, 'utf8_unicode_ci'), nullable=False)


class OroDictionaryRegion(Base):
    __tablename__ = 'oro_dictionary_region'

    combined_code = Column(String(16, 'utf8_unicode_ci'), primary_key=True)
    country_code = Column(ForeignKey('oro_dictionary_country.iso2_code'), index=True)
    code = Column(String(32, 'utf8_unicode_ci'), nullable=False)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)

    oro_dictionary_country = relationship('OroDictionaryCountry')


class OroDictionaryRegionTran(Base):
    __tablename__ = 'oro_dictionary_region_trans'
    __table_args__ = (
        Index('region_translation_idx', 'locale', 'object_class', 'field', 'foreign_key'),
    )

    id = Column(Integer, primary_key=True)
    foreign_key = Column(String(16, 'utf8_unicode_ci'), nullable=False)
    content = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    locale = Column(String(8, 'utf8_unicode_ci'), nullable=False)
    object_class = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    field = Column(String(32, 'utf8_unicode_ci'), nullable=False)


class OroEmail(Base):
    __tablename__ = 'oro_email'

    id = Column(Integer, primary_key=True)
    from_email_address_id = Column(ForeignKey('oro_email_address.id'), nullable=False, index=True)
    thread_id = Column(ForeignKey('oro_email_thread.id'), index=True)
    email_body_id = Column(ForeignKey('oro_email_body.id', ondelete='SET NULL'), unique=True)
    created = Column(DateTime, nullable=False)
    subject = Column(String(998, 'utf8_unicode_ci'), nullable=False)
    from_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    sent = Column(DateTime, nullable=False, index=True)
    importance = Column(Integer, nullable=False)
    internaldate = Column(DateTime, nullable=False)
    message_id = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    x_message_id = Column(String(255, 'utf8_unicode_ci'))
    x_thread_id = Column(String(255, 'utf8_unicode_ci'))
    is_head = Column(Integer, nullable=False, index=True, server_default=raw_text("1"))
    refs = Column(String(collation='utf8_unicode_ci'))
    multi_message_id = Column(String(collation='utf8_unicode_ci'))
    acceptLanguageHeader = Column(String(collation='utf8_unicode_ci'))
    body_synced = Column(Integer, server_default=raw_text("0"))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    email_body = relationship('OroEmailBody')
    from_email_address = relationship('OroEmailAddres')
    thread = relationship('OroEmailThread', primaryjoin='OroEmail.thread_id == OroEmailThread.id')
    users = relationship('OroUser', secondary='oro_rel_265353702da17977bb66fd')


class OroEmailAddres(Base):
    __tablename__ = 'oro_email_address'

    id = Column(Integer, primary_key=True)
    owner_mailbox_id = Column(ForeignKey('oro_email_mailbox.id'), index=True)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
    email = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    has_owner = Column(Integer, nullable=False)
    owner_user_id = Column(ForeignKey('oro_user.id'), index=True)

    owner_mailbox = relationship('OroEmailMailbox')
    owner_user = relationship('OroUser')


class OroEmailAttachment(Base):
    __tablename__ = 'oro_email_attachment'

    id = Column(Integer, primary_key=True)
    body_id = Column(ForeignKey('oro_email_body.id'), index=True)
    file_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    file_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    content_type = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    embedded_content_id = Column(String(255, 'utf8_unicode_ci'))

    body = relationship('OroEmailBody')
    file = relationship('OroAttachmentFile')


class OroEmailAttachmentContent(Base):
    __tablename__ = 'oro_email_attachment_content'

    id = Column(Integer, primary_key=True)
    attachment_id = Column(ForeignKey('oro_email_attachment.id'), nullable=False, unique=True)
    content = Column(String(collation='utf8_unicode_ci'), nullable=False)
    content_transfer_encoding = Column(String(20, 'utf8_unicode_ci'), nullable=False)

    attachment = relationship('OroEmailAttachment')


class OroEmailAutoResponseRule(Base):
    __tablename__ = 'oro_email_auto_response_rule'

    id = Column(Integer, primary_key=True)
    template_id = Column(ForeignKey('oro_email_template.id', ondelete='CASCADE'), index=True)
    mailbox_id = Column(ForeignKey('oro_email_mailbox.id', ondelete='CASCADE'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    active = Column(Integer, nullable=False)
    createdAt = Column(DateTime, nullable=False)
    definition = Column(String(collation='utf8_unicode_ci'))

    mailbox = relationship('OroEmailMailbox')
    template = relationship('OroEmailTemplate')


class OroEmailBody(Base):
    __tablename__ = 'oro_email_body'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    body = Column(String(collation='utf8_unicode_ci'), nullable=False)
    body_is_text = Column(Integer, nullable=False)
    has_attachments = Column(Integer, nullable=False)
    persistent = Column(Integer, nullable=False)
    text_body = Column(String(collation='utf8_unicode_ci'))


class OroEmailFolder(Base):
    __tablename__ = 'oro_email_folder'

    id = Column(Integer, primary_key=True)
    origin_id = Column(ForeignKey('oro_email_origin.id'), index=True)
    parent_folder_id = Column(ForeignKey('oro_email_folder.id', ondelete='CASCADE'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    full_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    type = Column(String(10, 'utf8_unicode_ci'), nullable=False)
    synchronized = Column(DateTime)
    outdated_at = Column(DateTime, index=True)
    sync_enabled = Column(Integer, nullable=False, server_default=raw_text("0"))
    sync_start_date = Column(DateTime)
    failed_count = Column(Integer, nullable=False, server_default=raw_text("0"))

    origin = relationship('OroEmailOrigin')
    parent_folder = relationship('OroEmailFolder', remote_side=[id])


class OroEmailFolderImap(Base):
    __tablename__ = 'oro_email_folder_imap'

    id = Column(Integer, primary_key=True)
    folder_id = Column(ForeignKey('oro_email_folder.id'), nullable=False, unique=True)
    uid_validity = Column(Integer, nullable=False)

    folder = relationship('OroEmailFolder')


class OroEmailImap(Base):
    __tablename__ = 'oro_email_imap'

    id = Column(Integer, primary_key=True)
    email_id = Column(ForeignKey('oro_email.id'), nullable=False, index=True)
    imap_folder_id = Column(ForeignKey('oro_email_folder_imap.id'), nullable=False, index=True)
    uid = Column(Integer, nullable=False)

    email = relationship('OroEmail')
    imap_folder = relationship('OroEmailFolderImap')


class OroEmailMailbox(Base):
    __tablename__ = 'oro_email_mailbox'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    process_settings_id = Column(ForeignKey('oro_email_mailbox_process.id'), unique=True)
    origin_id = Column(ForeignKey('oro_email_origin.id'), unique=True)
    email = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    label = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)

    organization = relationship('OroOrganization')
    origin = relationship('OroEmailOrigin')
    process_settings = relationship('OroEmailMailboxProces')
    roles = relationship('OroAccessRole', secondary='oro_email_mailbox_roles')
    users = relationship('OroUser', secondary='oro_email_mailbox_users')


class OroEmailMailboxProces(Base):
    __tablename__ = 'oro_email_mailbox_process'

    id = Column(Integer, primary_key=True)
    type = Column(String(30, 'utf8_unicode_ci'), nullable=False)


t_oro_email_mailbox_roles = Table(
    'oro_email_mailbox_roles', metadata,
    Column('mailbox_id', ForeignKey('oro_email_mailbox.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('role_id', ForeignKey('oro_access_role.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_oro_email_mailbox_users = Table(
    'oro_email_mailbox_users', metadata,
    Column('mailbox_id', ForeignKey('oro_email_mailbox.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('user_id', ForeignKey('oro_user.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


class OroEmailOrigin(Base):
    __tablename__ = 'oro_email_origin'
    __table_args__ = (
        Index('isActive_name_idx', 'isActive', 'name'),
    )

    id = Column(Integer, primary_key=True)
    isActive = Column(Integer, nullable=False)
    sync_code_updated = Column(DateTime)
    synchronized = Column(DateTime)
    sync_code = Column(Integer)
    name = Column(String(30, 'utf8_unicode_ci'), nullable=False)
    internal_name = Column(String(30, 'utf8_unicode_ci'))
    sync_count = Column(Integer)
    mailbox_name = Column(String(64, 'utf8_unicode_ci'), nullable=False, index=True, server_default=raw_text("''"))
    owner_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), index=True)
    imap_host = Column(String(255, 'utf8_unicode_ci'))
    imap_port = Column(Integer)
    imap_ssl = Column(String(3, 'utf8_unicode_ci'))
    imap_user = Column(String(100, 'utf8_unicode_ci'))
    imap_password = Column(String(collation='utf8_unicode_ci'))
    smtp_host = Column(String(255, 'utf8_unicode_ci'))
    smtp_port = Column(Integer)
    smtp_encryption = Column(String(3, 'utf8_unicode_ci'))
    access_token = Column(String(255, 'utf8_unicode_ci'))
    refresh_token = Column(String(255, 'utf8_unicode_ci'))
    access_token_expires_at = Column(DateTime)

    organization = relationship('OroOrganization')
    owner = relationship('OroUser')


class OroEmailRecipient(Base):
    __tablename__ = 'oro_email_recipient'
    __table_args__ = (
        Index('email_id_type_idx', 'email_id', 'type'),
    )

    id = Column(Integer, primary_key=True)
    email_address_id = Column(ForeignKey('oro_email_address.id'), nullable=False, index=True)
    email_id = Column(ForeignKey('oro_email.id', ondelete='CASCADE'))
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    type = Column(String(3, 'utf8_unicode_ci'), nullable=False)

    email_address = relationship('OroEmailAddres')
    email = relationship('OroEmail')


class OroEmailTemplate(Base):
    __tablename__ = 'oro_email_template'
    __table_args__ = (
        Index('UQ_NAME', 'name', 'entityName', unique=True),
    )

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    isSystem = Column(Integer, nullable=False, index=True)
    isEditable = Column(Integer, nullable=False)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    parent = Column(Integer)
    subject = Column(String(255, 'utf8_unicode_ci'))
    content = Column(String(collation='utf8_unicode_ci'))
    entityName = Column(String(255, 'utf8_unicode_ci'), index=True)
    type = Column(String(20, 'utf8_unicode_ci'), nullable=False)
    visible = Column(Integer, nullable=False, server_default=raw_text("1"))
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)

    organization = relationship('OroOrganization')
    user_owner = relationship('OroUser')


class OroEmailTemplateTranslation(Base):
    __tablename__ = 'oro_email_template_translation'
    __table_args__ = (
        Index('lookup_unique_idx', 'locale', 'object_id', 'field'),
    )

    id = Column(Integer, primary_key=True)
    object_id = Column(ForeignKey('oro_email_template.id', ondelete='CASCADE'), index=True)
    locale = Column(String(8, 'utf8_unicode_ci'), nullable=False)
    field = Column(String(32, 'utf8_unicode_ci'), nullable=False)
    content = Column(String(collation='utf8_unicode_ci'))

    object = relationship('OroEmailTemplate')


class OroEmailThread(Base):
    __tablename__ = 'oro_email_thread'

    id = Column(Integer, primary_key=True)
    last_unseen_email_id = Column(ForeignKey('oro_email.id'), index=True)
    created = Column(DateTime, nullable=False)

    last_unseen_email = relationship('OroEmail', primaryjoin='OroEmailThread.last_unseen_email_id == OroEmail.id')


class OroEmailUser(Base):
    __tablename__ = 'oro_email_user'
    __table_args__ = (
        Index('received_idx', 'received', 'is_seen', 'mailbox_owner_id'),
        Index('user_owner_id_mailbox_owner_id_organization_id', 'user_owner_id', 'mailbox_owner_id', 'organization_id'),
        Index('seen_idx', 'is_seen', 'mailbox_owner_id')
    )

    id = Column(Integer, primary_key=True)
    email_id = Column(ForeignKey('oro_email.id', ondelete='CASCADE'), nullable=False, index=True)
    mailbox_owner_id = Column(ForeignKey('oro_email_mailbox.id', ondelete='SET NULL'), index=True)
    created_at = Column(DateTime, nullable=False)
    received = Column(DateTime, nullable=False)
    is_seen = Column(Integer, nullable=False, server_default=raw_text("1"))
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    unsyncedFlagCount = Column(Integer, nullable=False, server_default=raw_text("0"))
    origin_id = Column(ForeignKey('oro_email_origin.id'), index=True)

    email = relationship('OroEmail')
    mailbox_owner = relationship('OroEmailMailbox')
    organization = relationship('OroOrganization')
    origin = relationship('OroEmailOrigin')
    user_owner = relationship('OroUser')
    folders = relationship('OroEmailFolder', secondary='oro_email_user_folders')


t_oro_email_user_folders = Table(
    'oro_email_user_folders', metadata,
    Column('email_user_id', ForeignKey('oro_email_user.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('folder_id', ForeignKey('oro_email_folder.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


class OroEmbeddedForm(Base):
    __tablename__ = 'oro_embedded_form'

    id = Column(String(255, 'utf8_unicode_ci'), primary_key=True)
    owner_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    title = Column(String(collation='utf8_unicode_ci'), nullable=False)
    css = Column(String(collation='utf8_unicode_ci'), nullable=False)
    form_type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    success_message = Column(String(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    allowed_domains = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    owner = relationship('OroOrganization')


class OroEntityConfig(Base):
    __tablename__ = 'oro_entity_config'

    id = Column(Integer, primary_key=True)
    class_name = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime)
    mode = Column(String(8, 'utf8_unicode_ci'), nullable=False)
    data = Column(String(collation='utf8_unicode_ci'))


class OroEntityConfigField(Base):
    __tablename__ = 'oro_entity_config_field'

    id = Column(Integer, primary_key=True)
    entity_id = Column(ForeignKey('oro_entity_config.id', ondelete='CASCADE'), index=True)
    field_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    type = Column(String(60, 'utf8_unicode_ci'), nullable=False)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime)
    mode = Column(String(8, 'utf8_unicode_ci'), nullable=False)
    data = Column(String(collation='utf8_unicode_ci'))

    entity = relationship('OroEntityConfig')


class OroEntityConfigIndexValue(Base):
    __tablename__ = 'oro_entity_config_index_value'
    __table_args__ = (
        Index('idx_entity_config_index_entity', 'scope', 'code', 'value', 'entity_id'),
        Index('idx_entity_config_index_field', 'scope', 'code', 'value', 'field_id')
    )

    id = Column(Integer, primary_key=True)
    entity_id = Column(ForeignKey('oro_entity_config.id', ondelete='CASCADE'), index=True)
    field_id = Column(ForeignKey('oro_entity_config_field.id', ondelete='CASCADE'), index=True)
    code = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    scope = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(255, 'utf8_unicode_ci'))

    entity = relationship('OroEntityConfig')
    field = relationship('OroEntityConfigField')


class OroEntityConfigLog(Base):
    __tablename__ = 'oro_entity_config_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), index=True)
    logged_at = Column(DateTime, nullable=False)

    user = relationship('OroUser')


class OroEntityConfigLogDiff(Base):
    __tablename__ = 'oro_entity_config_log_diff'

    id = Column(Integer, primary_key=True)
    log_id = Column(ForeignKey('oro_entity_config_log.id', ondelete='CASCADE'), index=True)
    class_name = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    field_name = Column(String(100, 'utf8_unicode_ci'))
    scope = Column(String(100, 'utf8_unicode_ci'))
    diff = Column(String(collation='utf8_unicode_ci'), nullable=False)

    log = relationship('OroEntityConfigLog')


class OroEntityFallbackValue(Base):
    __tablename__ = 'oro_entity_fallback_value'

    id = Column(Integer, primary_key=True)
    fallback = Column(String(64, 'utf8_unicode_ci'))
    scalar_value = Column(String(255, 'utf8_unicode_ci'))
    array_value = Column(String(collation='utf8_unicode_ci'))


class OroEnumAuthStatu(Base):
    __tablename__ = 'oro_enum_auth_status'

    id = Column(String(32, 'utf8_unicode_ci'), primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    priority = Column(Integer, nullable=False)
    is_default = Column(Integer, nullable=False)


class OroEnumCeAttendeeStatu(Base):
    __tablename__ = 'oro_enum_ce_attendee_status'

    id = Column(String(32, 'utf8_unicode_ci'), primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    priority = Column(Integer, nullable=False)
    is_default = Column(Integer, nullable=False)


class OroEnumCeAttendeeType(Base):
    __tablename__ = 'oro_enum_ce_attendee_type'

    id = Column(String(32, 'utf8_unicode_ci'), primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    priority = Column(Integer, nullable=False)
    is_default = Column(Integer, nullable=False)


class OroEnumValueTran(Base):
    __tablename__ = 'oro_enum_value_trans'
    __table_args__ = (
        Index('oro_enum_value_trans_idx', 'locale', 'object_class', 'field', 'foreign_key'),
    )

    id = Column(Integer, primary_key=True)
    foreign_key = Column(String(32, 'utf8_unicode_ci'), nullable=False)
    content = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    locale = Column(String(8, 'utf8_unicode_ci'), nullable=False)
    object_class = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    field = Column(String(4, 'utf8_unicode_ci'), nullable=False)


class OroFallbackLocalizationVal(Base):
    __tablename__ = 'oro_fallback_localization_val'

    id = Column(Integer, primary_key=True)
    localization_id = Column(ForeignKey('oro_localization.id', ondelete='CASCADE'), index=True)
    fallback = Column(String(64, 'utf8_unicode_ci'), index=True)
    string = Column(String(255, 'utf8_unicode_ci'), index=True)
    text = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    localization = relationship('OroLocalization')
    menu_updates = relationship('OroNavigationMenuUpd', secondary='oro_navigation_menu_upd_title')
    menu_updates1 = relationship('OroNavigationMenuUpd', secondary='oro_navigation_menu_upd_descr')


class OroGridAppearanceType(Base):
    __tablename__ = 'oro_grid_appearance_type'

    name = Column(String(32, 'utf8_unicode_ci'), primary_key=True)
    label = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    icon = Column(String(255, 'utf8_unicode_ci'), nullable=False)


class OroGridView(Base):
    __tablename__ = 'oro_grid_view'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    filtersData = Column(String(collation='utf8_unicode_ci'), nullable=False)
    sortersData = Column(String(collation='utf8_unicode_ci'), nullable=False)
    gridName = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    columnsData = Column(String(collation='utf8_unicode_ci'))
    appearanceType = Column(ForeignKey('oro_grid_appearance_type.name'), index=True)
    appearanceData = Column(String(collation='utf8_unicode_ci'))
    discr_type = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)

    oro_grid_appearance_type = relationship('OroGridAppearanceType')
    organization = relationship('OroOrganization')
    user_owner = relationship('OroUser')


class OroGridViewUserRel(Base):
    __tablename__ = 'oro_grid_view_user_rel'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    grid_view_id = Column(ForeignKey('oro_grid_view.id', ondelete='CASCADE'), index=True)
    alias = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    grid_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)

    grid_view = relationship('OroGridView')
    user = relationship('OroUser')


class OroIntegrationChannel(Base):
    __tablename__ = 'oro_integration_channel'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    transport_id = Column(ForeignKey('oro_integration_transport.id'), unique=True)
    default_user_owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    default_business_unit_owner_id = Column(ForeignKey('oro_business_unit.id', ondelete='SET NULL'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    connectors = Column(String(collation='utf8_unicode_ci'), nullable=False)
    synchronization_settings = Column(String(collation='utf8_unicode_ci'), nullable=False)
    mapping_settings = Column(String(collation='utf8_unicode_ci'), nullable=False)
    enabled = Column(Integer)
    edit_mode = Column(Integer, nullable=False, server_default=raw_text("3"))
    previously_enabled = Column(Integer)

    default_business_unit_owner = relationship('OroBusinessUnit')
    default_user_owner = relationship('OroUser')
    organization = relationship('OroOrganization')
    transport = relationship('OroIntegrationTransport')


class OroIntegrationChannelStatu(Base):
    __tablename__ = 'oro_integration_channel_status'
    __table_args__ = (
        Index('oro_intch_con_state_idx', 'connector', 'code'),
    )

    id = Column(Integer, primary_key=True)
    channel_id = Column(ForeignKey('oro_integration_channel.id', ondelete='CASCADE'), nullable=False, index=True)
    code = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    connector = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    message = Column(String(collation='utf8_unicode_ci'), nullable=False)
    date = Column(DateTime, nullable=False, index=True)
    data = Column(String(collation='utf8_unicode_ci'))

    channel = relationship('OroIntegrationChannel')


class OroIntegrationFieldsChange(Base):
    __tablename__ = 'oro_integration_fields_changes'
    __table_args__ = (
        Index('oro_integration_fields_changes_idx', 'entity_id', 'entity_class'),
    )

    id = Column(Integer, primary_key=True)
    entity_class = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    entity_id = Column(Integer, nullable=False)
    changed_fields = Column(String(collation='utf8_unicode_ci'), nullable=False)


class OroIntegrationTransport(Base):
    __tablename__ = 'oro_integration_transport'

    id = Column(Integer, primary_key=True)
    type = Column(String(30, 'utf8_unicode_ci'), nullable=False, index=True)


class OroLanguage(Base):
    __tablename__ = 'oro_language'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    code = Column(String(16, 'utf8_unicode_ci'), nullable=False, unique=True)
    enabled = Column(Integer, nullable=False, server_default=raw_text("0"))
    installed_build_date = Column(DateTime)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    organization = relationship('OroOrganization')
    user_owner = relationship('OroUser')


class OroLocalization(Base):
    __tablename__ = 'oro_localization'

    id = Column(Integer, primary_key=True)
    parent_id = Column(ForeignKey('oro_localization.id', ondelete='SET NULL'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    formatting_code = Column(String(16, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    language_id = Column(ForeignKey('oro_language.id'), nullable=False, index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    language = relationship('OroLanguage')
    parent = relationship('OroLocalization', remote_side=[id])
    localized_values = relationship('OroFallbackLocalizationVal', secondary='oro_localization_title')


t_oro_localization_title = Table(
    'oro_localization_title', metadata,
    Column('localization_id', ForeignKey('oro_localization.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('localized_value_id', ForeignKey('oro_fallback_localization_val.id', ondelete='CASCADE'), primary_key=True, nullable=False, unique=True)
)


class OroMessageQueue(Base):
    __tablename__ = 'oro_message_queue'

    id = Column(Integer, primary_key=True)
    body = Column(String(collation='utf8_unicode_ci'))
    headers = Column(String(collation='utf8_unicode_ci'))
    properties = Column(String(collation='utf8_unicode_ci'))
    consumer_id = Column(String(255, 'utf8_unicode_ci'), index=True)
    redelivered = Column(Integer)
    queue = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    priority = Column(SmallInteger, nullable=False, index=True)
    delayed_until = Column(Integer, index=True)


class OroMessageQueueJob(Base):
    __tablename__ = 'oro_message_queue_job'

    id = Column(Integer, primary_key=True)
    root_job_id = Column(ForeignKey('oro_message_queue_job.id', ondelete='CASCADE'), index=True)
    owner_id = Column(String(255, 'utf8_unicode_ci'))
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    status = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    interrupted = Column(Integer, nullable=False)
    unique = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    started_at = Column(DateTime)
    stopped_at = Column(DateTime)
    data = Column(String(collation='utf8_unicode_ci'))
    job_progress = Column(Float(asdecimal=True))

    root_job = relationship('OroMessageQueueJob', remote_side=[id])


t_oro_message_queue_job_unique = Table(
    'oro_message_queue_job_unique', metadata,
    Column('name', String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
)


class OroMigration(Base):
    __tablename__ = 'oro_migrations'

    id = Column(Integer, primary_key=True)
    bundle = Column(String(250, 'utf8_unicode_ci'), nullable=False, index=True)
    version = Column(String(250, 'utf8_unicode_ci'), nullable=False)
    loaded_at = Column(DateTime, nullable=False)


class OroMigrationsDatum(Base):
    __tablename__ = 'oro_migrations_data'

    id = Column(Integer, primary_key=True)
    class_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    loaded_at = Column(DateTime, nullable=False)
    version = Column(String(255, 'utf8_unicode_ci'))


class OroNavigationHistory(Base):
    __tablename__ = 'oro_navigation_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), nullable=False, index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    url = Column(String(1023, 'utf8_unicode_ci'), nullable=False)
    title = Column(String(collation='utf8_unicode_ci'), nullable=False)
    visited_at = Column(DateTime, nullable=False)
    visit_count = Column(Integer, nullable=False)
    route = Column(String(128, 'utf8_unicode_ci'), nullable=False, index=True)
    route_parameters = Column(String(collation='utf8_unicode_ci'), nullable=False)
    entity_id = Column(Integer, index=True)

    organization = relationship('OroOrganization')
    user = relationship('OroUser')


class OroNavigationItem(Base):
    __tablename__ = 'oro_navigation_item'
    __table_args__ = (
        Index('sorted_items_idx', 'user_id', 'position'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), nullable=False, index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    type = Column(String(10, 'utf8_unicode_ci'), nullable=False)
    url = Column(String(1023, 'utf8_unicode_ci'), nullable=False)
    title = Column(String(collation='utf8_unicode_ci'), nullable=False)
    position = Column(SmallInteger, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    organization = relationship('OroOrganization')
    user = relationship('OroUser')


class OroNavigationItemPinbar(Base):
    __tablename__ = 'oro_navigation_item_pinbar'

    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('oro_navigation_item.id', ondelete='CASCADE'), nullable=False, unique=True)
    maximized = Column(DateTime)

    item = relationship('OroNavigationItem')


class OroNavigationMenuUpd(Base):
    __tablename__ = 'oro_navigation_menu_upd'
    __table_args__ = (
        Index('oro_navigation_menu_upd_uidx', 'key', 'scope_id', 'menu', unique=True),
    )

    id = Column(Integer, primary_key=True)
    key = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    parent_key = Column(String(100, 'utf8_unicode_ci'))
    uri = Column(String(1023, 'utf8_unicode_ci'))
    menu = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    is_active = Column(Integer, nullable=False)
    priority = Column(Integer)
    icon = Column(String(150, 'utf8_unicode_ci'))
    is_divider = Column(Integer, nullable=False)
    is_custom = Column(Integer, nullable=False)
    scope_id = Column(ForeignKey('oro_scope.id'), nullable=False, index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    scope = relationship('OroScope')


t_oro_navigation_menu_upd_descr = Table(
    'oro_navigation_menu_upd_descr', metadata,
    Column('menu_update_id', ForeignKey('oro_navigation_menu_upd.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('localized_value_id', ForeignKey('oro_fallback_localization_val.id', ondelete='CASCADE'), primary_key=True, nullable=False, unique=True)
)


t_oro_navigation_menu_upd_title = Table(
    'oro_navigation_menu_upd_title', metadata,
    Column('menu_update_id', ForeignKey('oro_navigation_menu_upd.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('localized_value_id', ForeignKey('oro_fallback_localization_val.id', ondelete='CASCADE'), primary_key=True, nullable=False, unique=True)
)


class OroNavigationPagestate(Base):
    __tablename__ = 'oro_navigation_pagestate'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), nullable=False, index=True)
    page_id = Column(String(4000, 'utf8_unicode_ci'), nullable=False)
    page_hash = Column(String(32, 'utf8_unicode_ci'), nullable=False, unique=True)
    data = Column(String(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user = relationship('OroUser')


class OroNote(Base):
    __tablename__ = 'oro_note'

    id = Column(Integer, primary_key=True)
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    updated_by_user_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    message = Column(String(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    attachment_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    attachment = relationship('OroAttachmentFile')
    organization = relationship('OroOrganization')
    updated_by_user = relationship('OroUser', primaryjoin='OroNote.updated_by_user_id == OroUser.id')
    user_owner = relationship('OroUser', primaryjoin='OroNote.user_owner_id == OroUser.id')


class OroNotificationEmailNotif(Base):
    __tablename__ = 'oro_notification_email_notif'

    id = Column(Integer, primary_key=True)
    recipient_list_id = Column(ForeignKey('oro_notification_recip_list.id'), unique=True)
    template_id = Column(ForeignKey('oro_email_template.id', ondelete='SET NULL'), index=True)
    event_id = Column(ForeignKey('oro_notification_event.id'), index=True)
    entity_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)

    event = relationship('OroNotificationEvent')
    recipient_list = relationship('OroNotificationRecipList')
    template = relationship('OroEmailTemplate')


class OroNotificationEmailSpool(Base):
    __tablename__ = 'oro_notification_email_spool'

    id = Column(Integer, primary_key=True)
    status = Column(Integer, nullable=False, index=True)
    message = Column(String(collation='utf8_unicode_ci'), nullable=False)
    log_type = Column(String(255, 'utf8_unicode_ci'))


class OroNotificationEvent(Base):
    __tablename__ = 'oro_notification_event'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    description = Column(String(collation='utf8_unicode_ci'))


class OroNotificationMassNotif(Base):
    __tablename__ = 'oro_notification_mass_notif'

    id = Column(Integer, primary_key=True)
    email = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    sender = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    subject = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    body = Column(String(collation='utf8_unicode_ci'))
    scheduledAt = Column(DateTime, nullable=False)
    processedAt = Column(DateTime, nullable=False)
    status = Column(Integer, nullable=False)


t_oro_notification_recip_group = Table(
    'oro_notification_recip_group', metadata,
    Column('recipient_list_id', ForeignKey('oro_notification_recip_list.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('group_id', ForeignKey('oro_access_group.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


class OroNotificationRecipList(Base):
    __tablename__ = 'oro_notification_recip_list'

    id = Column(Integer, primary_key=True)
    email = Column(String(255, 'utf8_unicode_ci'))
    owner = Column(Integer)

    users = relationship('OroUser', secondary='oro_notification_recip_user')


t_oro_notification_recip_user = Table(
    'oro_notification_recip_user', metadata,
    Column('recipient_list_id', ForeignKey('oro_notification_recip_list.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('user_id', ForeignKey('oro_user.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


class OroOrganization(Base):
    __tablename__ = 'oro_organization'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    description = Column(String(collation='utf8_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    enabled = Column(Integer, nullable=False, server_default=raw_text("1"))
    logo_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    logo = relationship('OroAttachmentFile')
    users = relationship('OroUser', secondary='oro_user_organization')
    plant = relationship('ChemScanPlant', back_populates='orga')

class OroProcessDefinition(Base):
    __tablename__ = 'oro_process_definition'

    name = Column(String(255, 'utf8_unicode_ci'), primary_key=True)
    label = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    enabled = Column(Integer, nullable=False)
    related_entity = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    execution_order = Column(SmallInteger, nullable=False)
    exclude_definitions = Column(String(collation='utf8_unicode_ci'))
    actions_configuration = Column(String(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    pre_conditions_configuration = Column(String(collation='utf8_unicode_ci'))


class OroProcessJob(Base):
    __tablename__ = 'oro_process_job'

    id = Column(Integer, primary_key=True)
    process_trigger_id = Column(ForeignKey('oro_process_trigger.id', ondelete='CASCADE'), index=True)
    entity_id = Column(Integer)
    entity_hash = Column(String(255, 'utf8_unicode_ci'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    process_trigger = relationship('OroProcessTrigger')


class OroProcessTrigger(Base):
    __tablename__ = 'oro_process_trigger'
    __table_args__ = (
        Index('process_trigger_unique_idx', 'event', 'field', 'definition_name', 'cron', unique=True),
    )

    id = Column(Integer, primary_key=True)
    definition_name = Column(ForeignKey('oro_process_definition.name', ondelete='CASCADE'), index=True)
    event = Column(String(255, 'utf8_unicode_ci'))
    field = Column(String(255, 'utf8_unicode_ci'))
    queued = Column(Integer, nullable=False)
    time_shift = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    priority = Column(SmallInteger, nullable=False)
    cron = Column(String(100, 'utf8_unicode_ci'))

    oro_process_definition = relationship('OroProcessDefinition')


t_oro_rel_265353702da17977bb66fd = Table(
    'oro_rel_265353702da17977bb66fd', metadata,
    Column('email_id', ForeignKey('oro_email.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('user_id', ForeignKey('oro_user.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_oro_rel_c3990ba62da17977270bd6 = Table(
    'oro_rel_c3990ba62da17977270bd6', metadata,
    Column('activitylist_id', ForeignKey('oro_activity_list.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('user_id', ForeignKey('oro_user.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


class OroReminder(Base):
    __tablename__ = 'oro_reminder'

    id = Column(Integer, primary_key=True)
    recipient_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), index=True)
    sender_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    subject = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    start_at = Column(DateTime, nullable=False)
    expire_at = Column(DateTime, nullable=False)
    method = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    interval_number = Column(Integer, nullable=False)
    interval_unit = Column(String(1, 'utf8_unicode_ci'), nullable=False)
    state = Column(String(32, 'utf8_unicode_ci'), nullable=False, index=True)
    related_entity_id = Column(Integer, nullable=False)
    related_entity_classname = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    sent_at = Column(DateTime)
    failure_exception = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    recipient = relationship('OroUser', primaryjoin='OroReminder.recipient_id == OroUser.id')
    sender = relationship('OroUser', primaryjoin='OroReminder.sender_id == OroUser.id')


class OroReport(Base):
    __tablename__ = 'oro_report'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    type = Column(ForeignKey('oro_report_type.name'), index=True)
    business_unit_owner_id = Column(ForeignKey('oro_business_unit.id', ondelete='SET NULL'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(collation='utf8_unicode_ci'))
    entity = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    definition = Column(String(collation='utf8_unicode_ci'), nullable=False)
    createdat = Column(DateTime, nullable=False)
    updatedat = Column(DateTime, nullable=False)
    chart_options = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    business_unit_owner = relationship('OroBusinessUnit')
    organization = relationship('OroOrganization')
    oro_report_type = relationship('OroReportType')


class OroReportType(Base):
    __tablename__ = 'oro_report_type'

    name = Column(String(32, 'utf8_unicode_ci'), primary_key=True)
    label = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)


class OroScope(Base):
    __tablename__ = 'oro_scope'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='CASCADE'), index=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), index=True)
    localization_id = Column(ForeignKey('oro_localization.id', ondelete='CASCADE'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    localization = relationship('OroLocalization')
    organization = relationship('OroOrganization')
    user = relationship('OroUser')
    oro_workflow_definition = relationship('OroWorkflowDefinition', secondary='oro_workflow_scopes')


class OroSearchIndexDatetime(Base):
    __tablename__ = 'oro_search_index_datetime'

    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('oro_search_item.id', ondelete='CASCADE'), nullable=False, index=True)
    field = Column(String(250, 'utf8_unicode_ci'), nullable=False)
    value = Column(DateTime, nullable=False)

    item = relationship('OroSearchItem')


class OroSearchIndexDecimal(Base):
    __tablename__ = 'oro_search_index_decimal'

    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('oro_search_item.id', ondelete='CASCADE'), nullable=False, index=True)
    field = Column(String(250, 'utf8_unicode_ci'), nullable=False)
    value = Column(Numeric(10, 2), nullable=False)

    item = relationship('OroSearchItem')


class OroSearchIndexInteger(Base):
    __tablename__ = 'oro_search_index_integer'

    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('oro_search_item.id', ondelete='CASCADE'), nullable=False, index=True)
    field = Column(String(250, 'utf8_unicode_ci'), nullable=False)
    value = Column(Integer, nullable=False)

    item = relationship('OroSearchItem')


class OroSearchIndexText(Base):
    __tablename__ = 'oro_search_index_text'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False, index=True)
    field = Column(String(250, 'utf8_unicode_ci'), nullable=False)
    value = Column(String(collation='utf8_unicode_ci'), nullable=False, index=True)


class OroSearchItem(Base):
    __tablename__ = 'oro_search_item'
    __table_args__ = (
        Index('idx_entity', 'entity', 'record_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    entity = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    alias = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    record_id = Column(Integer)
    title = Column(String(255, 'utf8_unicode_ci'))
    changed = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class OroSearchQuery(Base):
    __tablename__ = 'oro_search_query'

    id = Column(Integer, primary_key=True)
    entity = Column(String(250, 'utf8_unicode_ci'), nullable=False)
    query = Column(String(collation='utf8_unicode_ci'), nullable=False)
    result_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)


t_oro_security_perm_apply_entity = Table(
    'oro_security_perm_apply_entity', metadata,
    Column('permission_id', ForeignKey('oro_security_permission.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('permission_entity_id', ForeignKey('oro_security_permission_entity.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_oro_security_perm_excl_entity = Table(
    'oro_security_perm_excl_entity', metadata,
    Column('permission_id', ForeignKey('oro_security_permission.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('permission_entity_id', ForeignKey('oro_security_permission_entity.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


class OroSecurityPermission(Base):
    __tablename__ = 'oro_security_permission'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    label = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    description = Column(String(255, 'utf8_unicode_ci'))
    is_apply_to_all = Column(Integer, nullable=False)
    group_names = Column(String(collation='utf8_unicode_ci'), nullable=False)


class OroSecurityPermissionEntity(Base):
    __tablename__ = 'oro_security_permission_entity'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)

    permissions = relationship('OroSecurityPermission', secondary='oro_security_perm_apply_entity')
    permissions1 = relationship('OroSecurityPermission', secondary='oro_security_perm_excl_entity')


class OroSegment(Base):
    __tablename__ = 'oro_segment'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    type = Column(ForeignKey('oro_segment_type.name'), nullable=False, index=True)
    business_unit_owner_id = Column(ForeignKey('oro_business_unit.id', ondelete='SET NULL'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    description = Column(String(collation='utf8_unicode_ci'))
    entity = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    definition = Column(String(collation='utf8_unicode_ci'), nullable=False)
    createdat = Column(DateTime, nullable=False)
    updatedat = Column(DateTime, nullable=False)
    last_run = Column(DateTime)
    records_limit = Column(Integer)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    business_unit_owner = relationship('OroBusinessUnit')
    organization = relationship('OroOrganization')
    oro_segment_type = relationship('OroSegmentType')


class OroSegmentSnapshot(Base):
    __tablename__ = 'oro_segment_snapshot'
    __table_args__ = (
        Index('uniq_43b8bb67db296aad81257d5d', 'segment_id', 'entity_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    segment_id = Column(ForeignKey('oro_segment.id', ondelete='CASCADE'), nullable=False, index=True)
    integer_entity_id = Column(Integer, index=True)
    entity_id = Column(String(255, 'utf8_unicode_ci'), index=True)
    createdat = Column(DateTime, nullable=False)

    segment = relationship('OroSegment')


class OroSegmentType(Base):
    __tablename__ = 'oro_segment_type'

    name = Column(String(32, 'utf8_unicode_ci'), primary_key=True)
    label = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)


class OroSession(Base):
    __tablename__ = 'oro_session'

    id = Column(VARBINARY(128), primary_key=True)
    sess_data = Column(LargeBinary, nullable=False)
    sess_time = Column(Integer, nullable=False)
    sess_lifetime = Column(Integer, nullable=False)


class OroSidebarState(Base):
    __tablename__ = 'oro_sidebar_state'
    __table_args__ = (
        Index('sidebar_state_unique_idx', 'user_id', 'position', unique=True),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), nullable=False, index=True)
    position = Column(String(13, 'utf8_unicode_ci'), nullable=False)
    state = Column(String(17, 'utf8_unicode_ci'), nullable=False)

    user = relationship('OroUser')


class OroSidebarWidget(Base):
    __tablename__ = 'oro_sidebar_widget'
    __table_args__ = (
        Index('sidebar_widgets_user_placement_idx', 'user_id', 'placement'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), nullable=False, index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    placement = Column(String(50, 'utf8_unicode_ci'), nullable=False)
    position = Column(SmallInteger, nullable=False, index=True)
    widget_name = Column(String(50, 'utf8_unicode_ci'), nullable=False)
    settings = Column(String(collation='utf8_unicode_ci'))
    state = Column(String(22, 'utf8_unicode_ci'), nullable=False)

    organization = relationship('OroOrganization')
    user = relationship('OroUser')


class OroSystemCalendar(Base):
    __tablename__ = 'oro_system_calendar'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    background_color = Column(String(7, 'utf8_unicode_ci'))
    is_public = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False, index=True)
    extend_description = Column(String(collation='utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')


class OroTagTag(Base):
    __tablename__ = 'oro_tag_tag'
    __table_args__ = (
        Index('name_organization_idx', 'name', 'organization_id'),
    )

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    name = Column(String(50, 'utf8_unicode_ci'), nullable=False)
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
    taxonomy_id = Column(ForeignKey('oro_tag_taxonomy.id', ondelete='SET NULL'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')
    taxonomy = relationship('OroTagTaxonomy')
    user_owner = relationship('OroUser')


class OroTagTagging(Base):
    __tablename__ = 'oro_tag_tagging'
    __table_args__ = (
        Index('tagging_idx', 'tag_id', 'entity_name', 'record_id', 'user_owner_id', unique=True),
        Index('entity_name_idx', 'entity_name', 'record_id')
    )

    id = Column(Integer, primary_key=True)
    tag_id = Column(ForeignKey('oro_tag_tag.id', ondelete='CASCADE'), index=True)
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    created = Column(DateTime, nullable=False)
    entity_name = Column(String(100, 'utf8_unicode_ci'), nullable=False)
    record_id = Column(Integer, nullable=False)

    tag = relationship('OroTagTag')
    user_owner = relationship('OroUser')


class OroTagTaxonomy(Base):
    __tablename__ = 'oro_tag_taxonomy'
    __table_args__ = (
        Index('tag_taxonomy_name_organization_idx', 'name', 'organization_id'),
    )

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    name = Column(String(50, 'utf8_unicode_ci'), nullable=False)
    background_color = Column(String(7, 'utf8_unicode_ci'))
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime, nullable=False)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')
    user_owner = relationship('OroUser')


class OroTrackingDatum(Base):
    __tablename__ = 'oro_tracking_data'

    id = Column(Integer, primary_key=True)
    event_id = Column(ForeignKey('oro_tracking_event.id', ondelete='CASCADE'), unique=True)
    data = Column(String(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)

    event = relationship('OroTrackingEvent')


class OroTrackingEvent(Base):
    __tablename__ = 'oro_tracking_event'

    id = Column(Integer, primary_key=True)
    website_id = Column(ForeignKey('oro_tracking_website.id', ondelete='CASCADE'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    value = Column(Float(asdecimal=True))
    user_identifier = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False, index=True)
    logged_at = Column(DateTime, nullable=False, index=True)
    url = Column(String(collation='utf8_unicode_ci'), nullable=False)
    title = Column(String(collation='utf8_unicode_ci'))
    code = Column(String(255, 'utf8_unicode_ci'), index=True)
    parsed = Column(Integer, nullable=False, index=True, server_default=raw_text("0"))

    website = relationship('OroTrackingWebsite')


class OroTrackingEventDictionary(Base):
    __tablename__ = 'oro_tracking_event_dictionary'

    id = Column(Integer, primary_key=True)
    website_id = Column(ForeignKey('oro_tracking_website.id', ondelete='CASCADE'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)

    website = relationship('OroTrackingWebsite')


class OroTrackingUniqueVisit(Base):
    __tablename__ = 'oro_tracking_unique_visit'
    __table_args__ = (
        Index('uvisit_action_date_idx', 'website_id', 'action_date'),
        Index('uvisit_user_by_date_idx', 'user_identifier', 'action_date')
    )

    id = Column(Integer, primary_key=True)
    website_id = Column(ForeignKey('oro_tracking_website.id', ondelete='CASCADE'), index=True)
    visit_count = Column(Integer, nullable=False)
    user_identifier = Column(String(32, 'utf8_unicode_ci'), nullable=False)
    action_date = Column(Date, nullable=False)

    website = relationship('OroTrackingWebsite')


class OroTrackingVisit(Base):
    __tablename__ = 'oro_tracking_visit'
    __table_args__ = (
        Index('website_first_action_time_idx', 'website_id', 'first_action_time'),
    )

    id = Column(Integer, primary_key=True)
    website_id = Column(ForeignKey('oro_tracking_website.id', ondelete='CASCADE'), index=True)
    visitor_uid = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    ip = Column(String(255, 'utf8_unicode_ci'))
    client = Column(String(255, 'utf8_unicode_ci'))
    client_type = Column(String(255, 'utf8_unicode_ci'))
    client_version = Column(String(255, 'utf8_unicode_ci'))
    os = Column(String(255, 'utf8_unicode_ci'))
    os_version = Column(String(255, 'utf8_unicode_ci'))
    desktop = Column(Integer)
    mobile = Column(Integer)
    bot = Column(Integer)
    user_identifier = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    first_action_time = Column(DateTime, nullable=False)
    last_action_time = Column(DateTime, nullable=False)
    parsing_count = Column(Integer, nullable=False, server_default=raw_text("0"))
    parsed_uid = Column(Integer, nullable=False, server_default=raw_text("0"))
    identifier_detected = Column(Integer, nullable=False, server_default=raw_text("0"))

    website = relationship('OroTrackingWebsite')


class OroTrackingVisitEvent(Base):
    __tablename__ = 'oro_tracking_visit_event'

    id = Column(Integer, primary_key=True)
    event_id = Column(ForeignKey('oro_tracking_event_dictionary.id', ondelete='CASCADE'), index=True)
    visit_id = Column(ForeignKey('oro_tracking_visit.id', ondelete='CASCADE'), index=True)
    web_event_id = Column(ForeignKey('oro_tracking_event.id'), unique=True)
    website_id = Column(ForeignKey('oro_tracking_website.id', ondelete='CASCADE'), index=True)
    parsing_count = Column(Integer, nullable=False, server_default=raw_text("0"))

    event = relationship('OroTrackingEventDictionary')
    visit = relationship('OroTrackingVisit')
    web_event = relationship('OroTrackingEvent')
    website = relationship('OroTrackingWebsite')


class OroTrackingWebsite(Base):
    __tablename__ = 'oro_tracking_website'

    id = Column(Integer, primary_key=True)
    user_owner_id = Column(ForeignKey('oro_user.id', ondelete='SET NULL'), index=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    identifier = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    url = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime)
    extend_description = Column(String(collation='utf8_unicode_ci'))

    organization = relationship('OroOrganization')
    user_owner = relationship('OroUser')


class OroTranslation(Base):
    __tablename__ = 'oro_translation'
    __table_args__ = (
        Index('language_key_uniq', 'language_id', 'translation_key_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    value = Column(String(collation='utf8_unicode_ci'))
    scope = Column(SmallInteger, nullable=False)
    translation_key_id = Column(ForeignKey('oro_translation_key.id', ondelete='CASCADE'), nullable=False, index=True)
    language_id = Column(ForeignKey('oro_language.id', ondelete='CASCADE'), nullable=False, index=True)

    language = relationship('OroLanguage')
    translation_key = relationship('OroTranslationKey')


class OroTranslationKey(Base):
    __tablename__ = 'oro_translation_key'
    __table_args__ = (
        Index('key_domain_uniq', 'key', 'domain', unique=True),
    )

    id = Column(Integer, primary_key=True)
    key = Column(String(255, 'utf8_bin'), nullable=False)
    domain = Column(String(255, 'utf8_bin'), nullable=False, server_default=raw_text("'messages'"))


class OroUser(Base):
    __tablename__ = 'oro_user'
    __table_args__ = (
        Index('user_first_name_last_name_idx', 'first_name', 'last_name'),
    )

    id = Column(Integer, primary_key=True)
    avatar_id = Column(ForeignKey('oro_attachment_file.id', ondelete='SET NULL'), index=True)
    business_unit_owner_id = Column(ForeignKey('oro_business_unit.id', ondelete='SET NULL'), index=True)
    status_id = Column(ForeignKey('oro_user_status.id'), unique=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    username = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    email = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)
    phone = Column(String(255, 'utf8_unicode_ci'), index=True)
    name_prefix = Column(String(255, 'utf8_unicode_ci'))
    first_name = Column(String(255, 'utf8_unicode_ci'))
    middle_name = Column(String(255, 'utf8_unicode_ci'))
    last_name = Column(String(255, 'utf8_unicode_ci'))
    name_suffix = Column(String(255, 'utf8_unicode_ci'))
    birthday = Column(Date)
    enabled = Column(Integer, nullable=False)
    salt = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    password = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    confirmation_token = Column(String(255, 'utf8_unicode_ci'))
    password_requested = Column(DateTime)
    last_login = Column(DateTime)
    login_count = Column(Integer, nullable=False, server_default=raw_text("0"))
    createdAt = Column(DateTime, nullable=False)
    updatedAt = Column(DateTime, nullable=False)
    title = Column(String(255, 'utf8_unicode_ci'))
    password_changed = Column(DateTime)
    googleId = Column(String(255, 'utf8_unicode_ci'), index=True)
    auth_status_id = Column(ForeignKey('oro_enum_auth_status.id', ondelete='SET NULL'), index=True)
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    auth_status = relationship('OroEnumAuthStatu')
    avatar = relationship('OroAttachmentFile', primaryjoin='OroUser.avatar_id == OroAttachmentFile.id')
    business_unit_owner = relationship('OroBusinessUnit')
    organization = relationship('OroOrganization')
    status = relationship('OroUserStatu', primaryjoin='OroUser.status_id == OroUserStatu.id')


t_oro_user_access_group = Table(
    'oro_user_access_group', metadata,
    Column('user_id', ForeignKey('oro_user.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('group_id', ForeignKey('oro_access_group.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_oro_user_access_group_role = Table(
    'oro_user_access_group_role', metadata,
    Column('group_id', ForeignKey('oro_access_group.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('role_id', ForeignKey('oro_access_role.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


t_oro_user_access_role = Table(
    'oro_user_access_role', metadata,
    Column('user_id', ForeignKey('oro_user.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('role_id', ForeignKey('oro_access_role.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


class OroUserApi(Base):
    __tablename__ = 'oro_user_api'

    id = Column(Integer, primary_key=True)
    organization_id = Column(ForeignKey('oro_organization.id', ondelete='SET NULL'), index=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), nullable=False, index=True)
    api_key = Column(String(255, 'utf8_unicode_ci'), nullable=False, unique=True)

    organization = relationship('OroOrganization')
    user = relationship('OroUser')


t_oro_user_business_unit = Table(
    'oro_user_business_unit', metadata,
    Column('user_id', ForeignKey('oro_user.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('business_unit_id', ForeignKey('oro_business_unit.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


class OroUserEmail(Base):
    __tablename__ = 'oro_user_email'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id'), index=True)
    email = Column(String(255, 'utf8_unicode_ci'), nullable=False)

    user = relationship('OroUser')


class OroUserImpersonation(Base):
    __tablename__ = 'oro_user_impersonation'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), nullable=False, index=True)
    token = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    expire_at = Column(DateTime, nullable=False)
    login_at = Column(DateTime)
    notify = Column(Integer, nullable=False, server_default=raw_text("0"))
    ip_address = Column(String(255, 'utf8_unicode_ci'), nullable=False, server_default=raw_text("'127.0.0.1'"))

    user = relationship('OroUser')


t_oro_user_organization = Table(
    'oro_user_organization', metadata,
    Column('user_id', ForeignKey('oro_user.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('organization_id', ForeignKey('oro_organization.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


class OroUserStatu(Base):
    __tablename__ = 'oro_user_status'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id'), index=True)
    status = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)

    user = relationship('OroUser', primaryjoin='OroUserStatu.user_id == OroUser.id')


class OroWindowsState(Base):
    __tablename__ = 'oro_windows_state'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('oro_user.id', ondelete='CASCADE'), nullable=False, index=True)
    data = Column(String(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user = relationship('OroUser')


class OroWorkflowDefinition(Base):
    __tablename__ = 'oro_workflow_definition'

    name = Column(String(255, 'utf8_unicode_ci'), primary_key=True)
    start_step_id = Column(ForeignKey('oro_workflow_step.id', ondelete='SET NULL'), index=True)
    label = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    related_entity = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    entity_attribute_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    steps_display_ordered = Column(Integer, nullable=False)
    system = Column(Integer, nullable=False)
    configuration = Column(String(collation='utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    active = Column(Integer, nullable=False, server_default=raw_text("0"))
    priority = Column(Integer, nullable=False, server_default=raw_text("0"))
    applications = Column(String(collation='utf8_unicode_ci'), nullable=False)
    exclusive_active_groups = Column(String(collation='utf8_unicode_ci'))
    exclusive_record_groups = Column(String(collation='utf8_unicode_ci'))

    start_step = relationship('OroWorkflowStep', primaryjoin='OroWorkflowDefinition.start_step_id == OroWorkflowStep.id')


class OroWorkflowEntityAcl(Base):
    __tablename__ = 'oro_workflow_entity_acl'
    __table_args__ = (
        Index('oro_workflow_acl_unique_idx', 'workflow_name', 'attribute', 'workflow_step_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    workflow_name = Column(ForeignKey('oro_workflow_definition.name', ondelete='CASCADE'), index=True)
    workflow_step_id = Column(ForeignKey('oro_workflow_step.id', ondelete='CASCADE'), index=True)
    attribute = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    entity_class = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    updatable = Column(Integer, nullable=False)
    deletable = Column(Integer, nullable=False)

    oro_workflow_definition = relationship('OroWorkflowDefinition')
    workflow_step = relationship('OroWorkflowStep')


class OroWorkflowEntityAclIdent(Base):
    __tablename__ = 'oro_workflow_entity_acl_ident'
    __table_args__ = (
        Index('oro_workflow_entity_acl_identity_unique_idx', 'workflow_entity_acl_id', 'entity_id', 'workflow_item_id', unique=True),
        Index('oro_workflow_entity_acl_identity_idx', 'entity_id', 'entity_class')
    )

    id = Column(Integer, primary_key=True)
    workflow_entity_acl_id = Column(ForeignKey('oro_workflow_entity_acl.id', ondelete='CASCADE'), index=True)
    workflow_item_id = Column(ForeignKey('oro_workflow_item.id', ondelete='CASCADE'), index=True)
    entity_class = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    entity_id = Column(Integer, nullable=False)

    workflow_entity_acl = relationship('OroWorkflowEntityAcl')
    workflow_item = relationship('OroWorkflowItem')


class OroWorkflowItem(Base):
    __tablename__ = 'oro_workflow_item'
    __table_args__ = (
        Index('oro_workflow_item_entity_idx', 'entity_class', 'entity_id'),
        Index('oro_workflow_item_entity_definition_unq', 'entity_id', 'workflow_name', unique=True)
    )

    id = Column(Integer, primary_key=True)
    current_step_id = Column(ForeignKey('oro_workflow_step.id', ondelete='SET NULL'), index=True)
    workflow_name = Column(ForeignKey('oro_workflow_definition.name', ondelete='CASCADE'), nullable=False, index=True)
    entity_id = Column(String(255, 'utf8_unicode_ci'))
    created = Column(DateTime, nullable=False)
    updated = Column(DateTime)
    data = Column(String(collation='utf8_unicode_ci'))
    entity_class = Column(String(255, 'utf8_unicode_ci'))
    serialized_data = Column(String(collation='utf8_unicode_ci'))

    current_step = relationship('OroWorkflowStep')
    oro_workflow_definition = relationship('OroWorkflowDefinition')


class OroWorkflowRestriction(Base):
    __tablename__ = 'oro_workflow_restriction'
    __table_args__ = (
        Index('oro_workflow_restriction_idx', 'workflow_name', 'workflow_step_id', 'field', 'entity_class', 'mode', unique=True),
    )

    id = Column(Integer, primary_key=True)
    workflow_step_id = Column(ForeignKey('oro_workflow_step.id', ondelete='CASCADE'), index=True)
    workflow_name = Column(ForeignKey('oro_workflow_definition.name', ondelete='CASCADE'), nullable=False, index=True)
    attribute = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    field = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    entity_class = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    mode = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    mode_values = Column(String(collation='utf8_unicode_ci'))

    oro_workflow_definition = relationship('OroWorkflowDefinition')
    workflow_step = relationship('OroWorkflowStep')


class OroWorkflowRestrictionIdent(Base):
    __tablename__ = 'oro_workflow_restriction_ident'
    __table_args__ = (
        Index('oro_workflow_restr_ident_unique_idx', 'workflow_restriction_id', 'entity_id', 'workflow_item_id', unique=True),
    )

    id = Column(Integer, primary_key=True)
    workflow_restriction_id = Column(ForeignKey('oro_workflow_restriction.id', ondelete='CASCADE'), index=True)
    workflow_item_id = Column(ForeignKey('oro_workflow_item.id', ondelete='CASCADE'), nullable=False, index=True)
    entity_id = Column(Integer, nullable=False, index=True)

    workflow_item = relationship('OroWorkflowItem')
    workflow_restriction = relationship('OroWorkflowRestriction')


t_oro_workflow_scopes = Table(
    'oro_workflow_scopes', metadata,
    Column('workflow_name', ForeignKey('oro_workflow_definition.name', ondelete='CASCADE'), primary_key=True, nullable=False, index=True),
    Column('scope_id', ForeignKey('oro_scope.id', ondelete='CASCADE'), primary_key=True, nullable=False, index=True)
)


class OroWorkflowStep(Base):
    __tablename__ = 'oro_workflow_step'
    __table_args__ = (
        Index('oro_workflow_step_unique_idx', 'workflow_name', 'name', unique=True),
    )

    id = Column(Integer, primary_key=True)
    workflow_name = Column(ForeignKey('oro_workflow_definition.name', ondelete='CASCADE'), index=True)
    name = Column(String(255, 'utf8_unicode_ci'), nullable=False, index=True)
    label = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    step_order = Column(Integer, nullable=False)
    is_final = Column(Integer, nullable=False)

    oro_workflow_definition = relationship('OroWorkflowDefinition', primaryjoin='OroWorkflowStep.workflow_name == OroWorkflowDefinition.name')


class OroWorkflowTransTrigger(Base):
    __tablename__ = 'oro_workflow_trans_trigger'

    id = Column(Integer, primary_key=True)
    workflow_name = Column(ForeignKey('oro_workflow_definition.name', ondelete='CASCADE'), nullable=False, index=True)
    entity_class = Column(String(255, 'utf8_unicode_ci'))
    queued = Column(Integer, nullable=False)
    transition_name = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    type = Column(String(255, 'utf8_unicode_ci'), nullable=False)
    cron = Column(String(100, 'utf8_unicode_ci'))
    filter = Column(String(collation='utf8_unicode_ci'))
    event = Column(String(255, 'utf8_unicode_ci'))
    field = Column(String(255, 'utf8_unicode_ci'))
    require = Column(String(collation='utf8_unicode_ci'))
    relation = Column(String(collation='utf8_unicode_ci'))

    oro_workflow_definition = relationship('OroWorkflowDefinition')


class OroWorkflowTransitionLog(Base):
    __tablename__ = 'oro_workflow_transition_log'

    id = Column(Integer, primary_key=True)
    step_from_id = Column(ForeignKey('oro_workflow_step.id', ondelete='SET NULL'), index=True)
    step_to_id = Column(ForeignKey('oro_workflow_step.id', ondelete='SET NULL'), index=True)
    workflow_item_id = Column(ForeignKey('oro_workflow_item.id', ondelete='CASCADE'), index=True)
    transition = Column(String(255, 'utf8_unicode_ci'))
    transition_date = Column(DateTime, nullable=False)

    step_from = relationship('OroWorkflowStep', primaryjoin='OroWorkflowTransitionLog.step_from_id == OroWorkflowStep.id')
    step_to = relationship('OroWorkflowStep', primaryjoin='OroWorkflowTransitionLog.step_to_id == OroWorkflowStep.id')
    workflow_item = relationship('OroWorkflowItem')
