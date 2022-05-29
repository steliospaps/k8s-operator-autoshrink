import os
import kopf
import time


def flip_timer(item):
    if(item['target-state'] == "original"):
        item['target-state'] = "zero"
    else:
        item['target-state'] = "original"

# name-> {last-check-time, cache-seconds, target-state: 'zero|original' }
target_is_zero={
    'test-timer': {'last-check-time': 0, 'cache-seconds': 10,'target-state': 'original', 'update_fun': flip_timer}
}

@kopf.timer('deployment',interval=6.0,
    labels={'autoshrink/zero-unless': kopf.PRESENT})
def autoshrink(spec, patch, status, labels, annotations, namespace, logger, **kwargs):
    #logger.info(f"spec={spec}")
    #logger.info(f"patch={patch}")
    #logger.info(f"kwargs={kwargs}")
    #logger.info(f"labels={labels}")
    #logger.info(f"status={status}")
    #logger.info(f"annotations={annotations}")

    style = labels['autoshrink/zero-unless']
    target = check_state(style,logger)
    if(target == "zero"):
        if(spec['replicas'] != 0):
            patch['spec']={'replicas': 0}
            patch['metadata']={'annotations': {'autoshrink/original-replicas': f"{spec['replicas']}"}}
            logger.info("moved to autoshrink target 'zero'")
    else:
        if(target == 'original'):
            oldReplicas=annotations.get('autoshrink/original-replicas','reverted')
            if(oldReplicas!= 'reverted'):
                patch['spec']={'replicas': int(oldReplicas)}
                patch['metadata']={'annotations': {'autoshrink/original-replicas': None }}
                logger.info("moved to autoshrink target 'original'")
def check_state(style, logger):
    if(style in target_is_zero):
        item=target_is_zero[style]
        now = time.time() # seconds
        if(item['last-check-time']+item['cache-seconds']<now):
            item['update_fun'](item)
            item['last-check-time']=now
            logger.info(f"updated item={item}")
        return item['target-state']
    else:
        return 'ignore'
