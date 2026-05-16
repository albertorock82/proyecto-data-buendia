import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions

def limpiar_datos(linea):
    # Simula la limpieza de registros (elimina la cabecera del CSV y separa campos)
    if "id_ticket" in linea:
        return None
    campos = linea.split(',')
    return {
        'id_ticket': campos[0],
        'fecha_venta': campos[1],
        'producto': campos[2],
        'cantidad': int(campos[3]),
        'precio_unitario': float(campos[4]),
        'sucursal': campos[5]
    }

def run():
    opciones = PipelineOptions()
    with beam.Pipeline(options=opciones) as pipeline:
        (
            pipeline

            | 'Leer CSV de Cloud Storage' >> beam.io.ReadFromText('gs://buendia-data-lake/*.csv')
            | 'Limpiar y Formatear' >> beam.Map(limpiar_datos)
            | 'Eliminar Nulos' >> beam.Filter(lambda x: x is not None)
            | 'Escribir en BigQuery' >> beam.io.WriteToBigQuery(
                'buendia-cafe:dataset_ventas.fact_ventas_diarias',
                write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )

if __name__ == '__main__':
    run()

