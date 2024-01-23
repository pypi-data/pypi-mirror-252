import labbench as lb


@attr.adjust('make', default='RIGOL TECHNOLOGIES')
@attr.adjust('model', default='MSO4014')
class RigolTechnologiesMSO4014(lb.VISADevice):
    pass


inst = RigolTechnologiesMSO4014('DS4C191000066')
