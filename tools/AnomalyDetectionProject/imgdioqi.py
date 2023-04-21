from matplotlib import pyplot as plt
import numpy as np
ssim=[0.9999828996166618, 0.9992755473827876, 0.9929415686901374, 0.9843544766890254, 0.9948090362406274, 0.9999949560566589, 0.9945319060907342, 0.9755571336331443, 0.994119379285112, 0.9799591159226545, 0.9940660554041497, 0.9718300509381117, 0.9943963988785767, 0.9979517821433328, 0.9904884504755516, 0.9889952445674575, 0.9951254287703035, 0.9905222120523389, 0.9961011029366293, 0.9853316755347737, 0.9999950712754448, 0.9947155462944322, 0.9948970603779598, 0.9775620503082515, 0.9952784691262433, 0.9785373015407712, 0.9951290598717017, 0.9873888310678035, 0.9999969874502441, 0.9859724035689851, 0.9956996438450564, 0.9846375181695736, 0.9991049325508027, 0.9802844166972515, 0.9944761114195579, 0.9785124354094386, 0.9946853669239474, 0.9745265547102201, 0.9903617848353237, 0.9768520041174353, 0.9914766296764852, 0.9546078101650067, 0.9764504178732796, 0.9421538115787562, 0.9999954206619124, 0.9769465796102148, 0.9889179868373058, 0.989667702334822, 0.994619285465646, 0.9676116643006554, 0.9995386142759922, 0.9850626991601202, 0.9971590895003203, 0.9978909347546799, 0.9846205894737966, 0.9601528615571481, 0.9906096996896361, 0.953387220847926, 0.9837957309282161, 0.9800899341587689, 0.9988472485796829, 0.9789732401759953, 0.9932552532277956, 0.9809821363675751, 0.9943280530428835, 0.9893758413719088, 0.9994659278352696, 0.9850381657624704, 0.999998109219381, 0.9996120990254064, 0.9960386380958381, 0.9986879878128526, 0.988990465471752, 0.9643685547938206, 0.9733507994867296, 0.9555287849606768]
ssim_align = [0.9999828996166618, 0.9992778451388739, 0.9939308024596519, 0.9852548333046204, 0.9920849320789287, 0.9999949560566589, 0.9953942238571665, 0.9676406616180719, 0.9919024987199416, 0.9886700490782221, 0.9945900198406544, 0.9644961481427544, 0.9956223560200755, 0.9980722653646555, 0.9920488824994205, 0.9890868896174614, 0.9961979003633643, 0.9924569088317301, 0.9961303066517471, 0.9857215805051749, 0.9999950712754448, 0.9954140781766898, 0.9910867690319727, 0.977805339752399, 0.9965853476662876, 0.981735469923622, 0.9958064735739413, 0.9698872464346608, 0.9999969874502441, 0.9882606668217381, 0.9958655423170436, 0.9847333971963121, 0.9991049325508027, 0.9876718300620306, 0.9898269559942822, 0.9790187269299933, 0.9960266515700194, 0.9829947112446584, 0.9919273706749864, 0.9773515393501689, 0.9914766296764852, 0.9535304248838017, 0.9780210460026674, 0.952106639729105, 0.9999954206619124, 0.9733966416446701, 0.9801881310689818, 0.9898580214456335, 0.9955378450944524, 0.9755214702222803, 0.9995290320984102, 0.982693256293103, 0.9971590895003203, 0.9979057474958106, 0.9863240617979653, 0.9698343612454742, 0.9906096996896361, 0.9565289899162179, 0.983763277245806, 0.9802178712044891, 0.9988472485796829, 0.9803126314168779, 0.9930963677444901, 0.982822122690705, 0.9955570552911138, 0.9906574510940312, 0.9994599196695505, 0.9850108236041161, 0.999998109219381, 0.9996124731135078, 0.9961974866171927, 0.9987242081659291, 0.9906937333789553, 0.9739371668721291, 0.9762311143981025, 0.9695387256727919]
x= list(range(1,len(ssim)+1,1))
print(x)
plt.plot(x,ssim,'s-',color = 'r',label="ssim")
plt.plot(x,ssim_align,'o-',color = 'g',label="ssim_align")
plt.xlabel("images")
plt.ylabel("ssim score")
plt.legend(loc = "best")
plt.show()