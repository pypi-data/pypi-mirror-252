from enum import Enum


class CodigoErrorAcuseServidor(str, Enum):
    datos_correcto = 'EA00'
    sistema_desconectado = 'EA01'
    cda_id_obligatorio = 'EA02'
    cda_id_duplicado = 'EA03'
    formato_hora_insercion_invalido = 'EA04'
    certificado_invalido = 'EA05'

    nombre_ordenante_excede_longitud = 'EB01'
    nombre_ordenante_invalido = 'EB02'
    nombre_ordenante_vacio = 'EB03'

    tipo_cuenta_ordenante_obligatorio = 'EC01'
    tipo_cuenta_ordenante_invalida = 'EC02'

    cuenta_ordenante_obligatorio = 'ED01'
    cuenta_ordenante_solo_numerica = 'ED02'
    cuenta_ordenante_excede_longitud = 'ED03'
    cuenta_ordenante_solo_ceros = 'ED04'

    rfc_ordenante_excede_longitud = 'EE01'
    rfc_ordenante_invalido = 'EE02'
    rfc_rodenante_vacio = 'EE03'

    nombre_beneficiario_excede_longitud = 'EF01'
    nombre_beneficiario_invalido = 'EF02'
    nombre_beneficiario_vacio = 'EF03'
    nombre_beneficiario_2_excede_longitud = 'EF04'
    nombre_beneficiario_2_invalido = 'EF05'
    nombre_beneficiario_2_vacio = 'EF06'

    tipo_cuenta_beneficiario_obligatorio = 'EG01'
    tipo_cuenta_beneficiario_invalido = 'EG02'
    tipo_cuenta_beneficiario_2_obligatorio = 'EG03'
    tipo_cuenta_beneficiario_2_invalido = 'EG04'

    cuenta_beneficiario_obligatoria = 'EH01'
    cuenta_beneficiario_solo_numerica = 'EH02'
    cuenta_beneficiario_excede_longitud = 'EH03'
    cuenta_beneficiario_solo_ceros = 'EH04'
    cuenta_beneficiario_2_obligatoria = 'EH05'
    cuenta_beneficiario_2_solo_numerica = 'EH06'
    cuenta_beneficiario_2_excede_longitud = 'EH07'
    cuenta_beneficiario_2_solo_ceros = 'EH08'

    rfc_beneficiario_excede_longitud = 'EI01'
    rfc_beneficiario_invalido = 'EI2'
    rfc_beneficiario_vacio = 'EI03'
    rfc_beneficiario_2_excede_longitud = 'EI04'
    rfc_beneficiario_2_invalido = 'EI05'
    rfc_beneficiario_2_vacio = 'EI06'

    concepto_pago_excede_longitud = 'EJ01'
    concepto_pago_invalido = 'EJ02'
    concepto_pago_vacio = 'EJ03'

    iva_no_permitido = 'EK01'
    formato_iva_incorrecto = 'EK02'

    monto_obligatorio = 'EL01'
    monto_no_permitido = 'EL02'
    formato_monto_incorrecto = 'EL03'
    monto_comision_obligatorio = 'EL04'
    monto_comision_invalido = 'EL05'
    monto_comision_no_permitido = 'EL06'

    clave_rastreo_excede_longitud = 'EM01'
    clave_rastreo_invalida = 'EM02'
    clave_rastreo_vacia = 'EM03'
    clave_rastreo_obligatoria = 'EM04'

    fecha_operacion_obligatoria = 'EN01'
    formato_fecha_operacion_invalido = 'EN02'
    fecha_operacion_no_coincide_fecha_sistema = 'EN03'
    hora_operacion_obligatoria = 'EN04'
    formato_hora_operacion_invalido = 'EN05'

    clave_emisor_obligatoria = 'EO01'
    clave_emisor_invalida = 'EO02'

    nombre_institucion_emisora_obligatorio = 'EP01'
    nombre_institucion_emisora_invalida = 'EP02'
    nombre_institucion_receptora_obligatorio = 'EP03'
    nombre_institucion_receptora_invalida = 'EP04'
    nombre_institucion_emisora_coincide_nombre_institucion_receptora = 'EP05'

    envio_resultado = 'EQ00'

    mensaje_xml_invalido = 'ER01'
    informacion_no_encontrada = 'ES01'
    folio_pago_original_invalido = 'ET01'
    folio_paquete_original_invalido = 'ET02'
    tipo_pago_obligatorio = 'EV01'
    tipo_pago_invalido = 'EV02'
    clasificacion_operacion_obligatoria = 'EW01'
    clasificacion_operacion_maximo_2_digitos = 'EW02'

    folio_codi_no_corresponde = 'EY01'
    folio_codi_invalido = 'EY02'
    folio_codi_obligatorio = 'EY03'
    pago_comision_obligatorio = 'EU01'
    pago_comision_excede_longitud = 'EU02'
    pago_comision_invalido = 'EU03'


class CodigoErrorAcuseBanxico(str, Enum):
    exito = '0'
    datos_cda_incorrectos = '1'
    fecha_operacion_incorrecta = '2'
    participantes_invalidos = '5'
    paquete_folio_invalido = '6'
    folio_invalido = '7'
    formato_hora_incorrecto = '12'
    tipo_mensaje_invalido = '26'
    cda_excede_longitud = '34'
    tipo_mensaje_no_aceptado = '36'
    clave_participante_cda_invalida = '37'
    clave_participante_orden_invalida = '38'
    orden_no_encontrada = '43'
    formato_cda_incorrecto = '44'
    monto_iva_incorrecto = '45'
    firma_invalida = '47'
    cda_duplicada = '54'
    monto_cda_incorrecto = '55'
    tipo_pago_incorrecto = '56'
