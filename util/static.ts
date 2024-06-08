import { RegionKey } from './types/types'

export const RegionTimeZoneMapping: { [K in RegionKey]: string } = {
  'NA West': 'UTC-7',
  'NA East': 'UTC-4',
  'EU Central': 'UTC+2'
}
