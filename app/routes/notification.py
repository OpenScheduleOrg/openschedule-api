from datetime import datetime, time, date, timedelta
import calendar

from flask import request, jsonify
from sqlalchemy import desc

from . import bp_api
from ..models import session, select, update, Cliente, Notification
from ..exceptions import APIExceptionHandler
from ..utils import useless_params

# GET clinicas #


@bp_api.route("/notifications", methods=["GET"])
def get_notifications(id=None):

    stmt = select(Notification.id, Notification.message,
                  Cliente.telefone).where(Notification.send == False).order_by(
                      Notification.created_at)

    notifications_result = session.execute(stmt).all()

    session.execute(
        update(Notification).values(send=True).where(
            Notification.id.in_([noti[0] for noti in notifications_result])))
    session.commit()

    notifications = {}

    for noti in notifications_result:
        if noti[2] not in notifications: notifications[noti[2]] = []
        notifications[noti[2]].append(noti[1])

    return jsonify(status="success", data={"notifications":
                                           notifications}), 200


# END GET clinicas #
